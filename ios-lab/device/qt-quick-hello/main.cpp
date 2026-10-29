#include <QDir>
#include <QFile>
#include <QGuiApplication>
#include <QJsonDocument>
#include <QJsonObject>
#include <QQmlApplicationEngine>
#include <QQuickStyle>
#include <QQuickWindow>
#include <QSGRendererInterface>
#include <QStandardPaths>
#include <QTimer>
#include <cstdio>

int main(int argc, char **argv)
{
    QGuiApplication app(argc, argv);
    const auto logDirectory = QStandardPaths::writableLocation(QStandardPaths::DocumentsLocation);
    QDir().mkpath(logDirectory);
    freopen(qPrintable(logDirectory + QStringLiteral("/qt-quick-runtime.log")), "w", stderr);
    qInstallMessageHandler([](QtMsgType type, const QMessageLogContext &context, const QString &message) {
        fprintf(stderr, "%s\n", qPrintable(qFormatLogMessage(type, context, message)));
        fflush(stderr);
    });
    app.setApplicationVersion(QString::fromLatin1(qVersion()));
    QQuickStyle::setStyle(QStringLiteral("Material"));
    QQmlApplicationEngine engine;
    engine.loadFromModule(QStringLiteral("PhoneHello"), QStringLiteral("Main"));
    if (engine.rootObjects().isEmpty())
        return 2;
    auto *window = qobject_cast<QQuickWindow *>(engine.rootObjects().first());
    if (!window)
        return 3;
    QTimer diagnostics;
    QObject::connect(&diagnostics, &QTimer::timeout, window, [window] {
        const auto directory = QStandardPaths::writableLocation(QStandardPaths::DocumentsLocation);
        QDir().mkpath(directory);
        const auto image = window->grabWindow();
        const bool saved = !image.isNull() && image.save(directory + QStringLiteral("/qt-quick-phone.png"));
        const auto api = window->rendererInterface()->graphicsApi();
        QJsonObject result{{"qt_version", QString::fromLatin1(qVersion())},
                           {"qml_window_visible", window->isVisible()},
                           {"graphics_api", int(api)},
                           {"metal", api == QSGRendererInterface::Metal},
                           {"taps", window->property("taps").toInt()},
                           {"rendered_snapshot_saved", saved},
                           {"image_width", image.width()}, {"image_height", image.height()}};
        QFile output(directory + QStringLiteral("/qt-quick-phone-result.json"));
        if (output.open(QIODevice::WriteOnly))
            output.write(QJsonDocument(result).toJson());
    });
    diagnostics.start(2000);
    return app.exec();
}
