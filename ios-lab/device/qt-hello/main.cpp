#include <QApplication>
#include <QDir>
#include <QFile>
#include <QJsonDocument>
#include <QJsonObject>
#include <QLoggingCategory>
#include <QLabel>
#include <QMutex>
#include <QStandardPaths>
#include <QSysInfo>
#include <QTimer>
#include <QWindow>
#include <thread>
#include <vector>

void configurePhoneDiagnostics();
QJsonObject phoneWindowState(quintptr viewId);

int main(int argc, char **argv)
{
    configurePhoneDiagnostics();
    qInstallMessageHandler([](QtMsgType type, const QMessageLogContext &context, const QString &message) {
        fprintf(stderr, "%s\n", qPrintable(qFormatLogMessage(type, context, message)));
        fflush(stderr);
    });
    QLoggingCategory::setFilterRules(QStringLiteral("qt.qpa.*=true\nqt.rhi.*=true\nqt.widgets.painting=true"));
    QApplication app(argc, argv);
    QMutex mutex;
    int count = 0;
    std::vector<std::thread> workers;
    for (int i = 0; i < 4; ++i) {
        workers.emplace_back([&] {
            for (int j = 0; j < 5000; ++j) {
                QMutexLocker locker(&mutex);
                ++count;
                std::this_thread::yield();
            }
        });
    }
    for (auto &worker : workers)
        worker.join();
    if (count != 20000)
        return 2;

    QLabel label(QStringLiteral("Hello Qt %1!\nRunning on your iPhone 7.\n\niOS 15 compatibility build")
                 .arg(QString::fromLatin1(qVersion())));
    label.setAlignment(Qt::AlignCenter);
    label.setWordWrap(true);
    label.setStyleSheet(QStringLiteral("QLabel { background: #172234; color: #eaf2ff; font-size: 22px; padding: 16px; }"));
    label.resize(375, 667);
    label.show();
    QTimer::singleShot(500, &label, [&] { label.activateWindow(); label.raise(); });
    QTimer diagnostics;
    QObject::connect(&diagnostics, &QTimer::timeout, &label, [&] {
        const auto directory = QStandardPaths::writableLocation(QStandardPaths::DocumentsLocation);
        QDir().mkpath(directory);
        const bool imageSaved = label.grab().save(directory + QStringLiteral("/qt-phone-hello.png"));
        QJsonObject result{{"qt_version", QString::fromLatin1(qVersion())},
                           {"os_version", QSysInfo::productVersion()},
                           {"architecture", QSysInfo::currentCpuArchitecture()},
                           {"mutex_counter", count}, {"widget_visible", label.isVisible()},
                           {"widget_snapshot_saved", imageSaved}};
        result["native_window_exposed"] = label.windowHandle()->isExposed();
        result["application_active"] = app.applicationState() == Qt::ApplicationActive;
        result["uikit"] = phoneWindowState(label.winId());
        QFile output(directory + QStringLiteral("/qt-phone-result.json"));
        if (output.open(QIODevice::WriteOnly))
            output.write(QJsonDocument(result).toJson());
    });
    diagnostics.start(2000);
    return app.exec();
}
