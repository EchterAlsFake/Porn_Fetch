/* Local file stream-copy remux, based on FFmpeg's doc/examples/remuxing.c.
 * No subprocesses, decoders for video playback, encoders, or network access.
 */
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <libavformat/avformat.h>
#include <libavutil/avutil.h>
#include <libavutil/mem.h>
#include <libavutil/error.h>

static int remux(const char *input, const char *output, AVDictionary *tags,
                 const char *thumbnail, int64_t *packets) {
    AVFormatContext *in = NULL, *out = NULL, *cover = NULL;
    AVPacket *packet = av_packet_alloc(), *picture = av_packet_alloc();
    AVDictionary *options = NULL;
    int *mapping = NULL, result = AVERROR(ENOMEM), cover_index = -1;
    if (!packet || !picture) goto done;
    if ((result = avformat_open_input(&in, input, NULL, NULL)) < 0) goto done;
    if ((result = avformat_find_stream_info(in, NULL)) < 0) goto done;
    if ((result = avformat_alloc_output_context2(&out, NULL, "mp4", output)) < 0) goto done;
    mapping = av_malloc_array(in->nb_streams, sizeof(*mapping));
    if (!mapping) { result = AVERROR(ENOMEM); goto done; }
    av_dict_copy(&out->metadata, in->metadata, 0);
    av_dict_copy(&out->metadata, tags, 0);
    for (unsigned i = 0; i < in->nb_streams; i++) {
        AVStream *src = in->streams[i];
        mapping[i] = -1;
        if (src->codecpar->codec_type != AVMEDIA_TYPE_VIDEO &&
            src->codecpar->codec_type != AVMEDIA_TYPE_AUDIO) continue;
        /* Replace old cover art only when an explicit replacement is supplied. */
        if (thumbnail && (src->disposition & AV_DISPOSITION_ATTACHED_PIC)) continue;
        AVStream *dst = avformat_new_stream(out, NULL);
        if (!dst) { result = AVERROR(ENOMEM); goto done; }
        mapping[i] = dst->index;
        if ((result = avcodec_parameters_copy(dst->codecpar, src->codecpar)) < 0) goto done;
        dst->codecpar->codec_tag = 0;
        dst->time_base = src->time_base;
        dst->disposition = src->disposition;
        av_dict_copy(&dst->metadata, src->metadata, 0);
    }
    if (thumbnail) {
        if ((result = avformat_open_input(&cover, thumbnail, NULL, NULL)) < 0) goto done;
        if ((result = avformat_find_stream_info(cover, NULL)) < 0) goto done;
        if ((result = av_read_frame(cover, picture)) < 0) goto done;
        AVStream *src = cover->streams[picture->stream_index];
        if (src->codecpar->codec_id != AV_CODEC_ID_MJPEG && src->codecpar->codec_id != AV_CODEC_ID_PNG) {
            result = AVERROR(EINVAL); goto done;
        }
        AVStream *dst = avformat_new_stream(out, NULL);
        if (!dst) { result = AVERROR(ENOMEM); goto done; }
        if ((result = avcodec_parameters_copy(dst->codecpar, src->codecpar)) < 0) goto done;
        dst->codecpar->codec_tag = 0;
        dst->disposition = AV_DISPOSITION_ATTACHED_PIC;
        dst->time_base = (AVRational){1, 90000};
        cover_index = dst->index;
    }
    out->avoid_negative_ts = AVFMT_AVOID_NEG_TS_MAKE_NON_NEGATIVE;
    if ((result = avio_open(&out->pb, output, AVIO_FLAG_WRITE)) < 0) goto done;
    av_dict_set(&options, "movflags", "+faststart", 0);
    if ((result = avformat_write_header(out, &options)) < 0) goto done;
    if (cover_index >= 0) {
        picture->stream_index = cover_index;
        picture->pts = picture->dts = 0;
        picture->duration = 0;
        picture->pos = -1;
        if ((result = av_interleaved_write_frame(out, picture)) < 0) goto done;
    }
    while ((result = av_read_frame(in, packet)) >= 0) {
        AVStream *src = in->streams[packet->stream_index];
        int index = mapping[packet->stream_index];
        if (index < 0) { av_packet_unref(packet); continue; }
        AVStream *dst = out->streams[index];
        /* Normalize the common timeline while preserving audio/video offsets. */
        if (in->start_time != AV_NOPTS_VALUE) {
            int64_t start = av_rescale_q(in->start_time, AV_TIME_BASE_Q, src->time_base);
            if (packet->pts != AV_NOPTS_VALUE) packet->pts -= start;
            if (packet->dts != AV_NOPTS_VALUE) packet->dts -= start;
        }
        av_packet_rescale_ts(packet, src->time_base, dst->time_base);
        packet->stream_index = index;
        packet->pos = -1;
        result = av_interleaved_write_frame(out, packet);
        av_packet_unref(packet);
        if (result < 0) goto done;
        (*packets)++;
    }
    if (result == AVERROR_EOF) result = av_write_trailer(out);
done:
    av_dict_free(&options);
    av_packet_free(&packet);
    av_packet_free(&picture);
    av_free(mapping);
    avformat_close_input(&cover);
    avformat_close_input(&in);
    if (out) {
        if (out->pb) avio_closep(&out->pb);
        avformat_free_context(out);
    }
    return result;
}

static PyObject *python_remux(PyObject *self, PyObject *args) {
    const char *input, *output, *thumbnail = NULL;
    PyObject *metadata = NULL, *key, *value;
    Py_ssize_t position = 0;
    AVDictionary *tags = NULL;
    int64_t packets = 0;
    int result;
    if (!PyArg_ParseTuple(args, "ssO!z", &input, &output, &PyDict_Type, &metadata, &thumbnail)) return NULL;
    while (PyDict_Next(metadata, &position, &key, &value)) {
        const char *k = PyUnicode_AsUTF8(key), *v = PyUnicode_AsUTF8(value);
        if (!k || !v) { av_dict_free(&tags); return NULL; }
        if (av_dict_set(&tags, k, v, 0) < 0) { av_dict_free(&tags); return PyErr_NoMemory(); }
    }
    Py_BEGIN_ALLOW_THREADS
    result = remux(input, output, tags, thumbnail, &packets);
    av_dict_free(&tags);
    Py_END_ALLOW_THREADS
    if (result < 0) {
        char error[AV_ERROR_MAX_STRING_SIZE];
        av_strerror(result, error, sizeof(error));
        PyErr_Format(PyExc_RuntimeError, "FFmpeg remux failed: %s (%d)", error, result);
        return NULL;
    }
    return PyLong_FromLongLong(packets);
}
extern PyObject *ios_media_probe(PyObject *, PyObject *);
static PyMethodDef methods[] = {
    {"remux", python_remux, METH_VARARGS, "Stream-copy local media into faststart MP4."},
    {"apple_probe", ios_media_probe, METH_VARARGS, "Read native AVFoundation playback capability."}, {NULL}};
static struct PyModuleDef module = {PyModuleDef_HEAD_INIT, "_ios_ffmpeg", NULL, -1, methods};
PyMODINIT_FUNC PyInit__ios_ffmpeg(void) {
    PyObject *m = PyModule_Create(&module);
    if (m) { PyModule_AddStringConstant(m, "version", av_version_info());
             PyModule_AddStringConstant(m, "license", avformat_license()); }
    return m;
}
