#include "myconfig.h"
#include <QFileInfo>
#include <QJsonDocument>
#include <QJsonParseError>
#include <QMessageBox>

MyConfig::MyConfig()
{
    this->default_init();
    this->dump("./config.json");
};

MyConfig::MyConfig(const QString& config_file_str)
{
    QFile config_file(config_file_str);
    QFileInfo config_file_info(config_file);
    QString suffix = config_file_info.suffix();
    config_file.open(QIODevice::ReadOnly);
    QByteArray data = config_file.readAll();
    config_file.close();
    if (suffix == "json")
    {
        QJsonParseError parseError;
        QJsonDocument doc = QJsonDocument::fromJson(data, &parseError);
        if (parseError.error != QJsonParseError::NoError)
        {
            qDebug() << QStringLiteral("配置文件载入错误!使用默认配置");
            this->default_init();
            this->dump("./config_template.json");
            return;
        }
        QJsonObject obj = doc.object();
        new (this) MyConfig(obj);
    };
    this->load_eyetracker();
};

MyConfig::MyConfig(const QJsonObject& config_in_qjson)
{
    this->config_params = config_in_qjson.toVariantHash();
    this->config_source.append("QJsonObject");
    this->load_eyetracker();
};

MyConfig::~MyConfig()
{
    if (this->eyetracker_wrapper)
        delete this->eyetracker_wrapper;
};

void MyConfig::default_init()
{
    QString json_config_str = "{\"eyetracker\": {\"frequency\": 60,\"calibration_point_number\": 9},"
                              "\"database\": {\"path\": \"./imgdb\"},\"data\": {\"path\": \"./outdata\"},"
                              "\"log\": {\"path\": \"./log\"},\"image_show\": {\"last_time\": 8,\"time_interval\": 2},"
                              "\"mode\": {\"debug\": false}}";
    QJsonParseError parseError;
    QJsonDocument json_doc = QJsonDocument::fromJson(json_config_str.toUtf8(), &parseError);
    QJsonObject json_config = json_doc.object();
    this->config_params = json_config.toVariantHash();
    this->config_source = "default";
    this->load_eyetracker();
};

void MyConfig::load_eyetracker(const QString &address)
{
    this->eyetracker_wrapper = new EyeTrackerWrapper(address);
};

void MyConfig::set_value(const QString &key, const QVariant value)
{
    QStringList skeys = key.split('/');
    if (skeys.size() == 1)
    {
        if (this->config_params.contains(key))
            config_params[key] = value;
        else
            qCritical()<<QString("您设置的参数%1不存在").arg(key);
    }else if(skeys.size() == 2){
        QVariantHash ht;
        if(config_params[skeys[0]].canConvert<QVariantHash>()){
            ht = config_params[skeys[0]].toHash();
        }
        ht[skeys[1]] = value;
        config_params[skeys[0]] = ht;
    }else{
        qCritical()<<QString("本程序暂不支持两层以上嵌套配置");
    }
};

QVariant MyConfig::get_value(const QString &key, const QVariant default_value) const
{
    QStringList skeys = key.split('/');
    if (skeys.size() == 1)
    {
        if (this->config_params.contains(key))
            return this->config_params[key];
        else
            return default_value;
    }
    QVariant value = this->config_params[skeys[0]];
    int idx = 1;
    while (idx < skeys.size() - 1)
    {
        if (value.toHash().contains(skeys[idx]))
        {
            value = value.toHash()[skeys[idx]];
            idx++;
        }
        else
            return default_value;
    }
    return value.toHash()[skeys[idx]];
};

EyeTrackerWrapper *MyConfig::get_eyetracker_wrapper() const
{
    return this->eyetracker_wrapper;
}

void MyConfig::dump(const QString &fileName) const
{
    QFile file(fileName);
    QJsonObject obj = QJsonObject::fromVariantHash(this->config_params);
    QJsonDocument doc(obj);
    bool ok = file.open(QIODevice::WriteOnly);
    if (ok)
    {
        file.write(doc.toJson());
        file.close();
    }
    else
    {
        qDebug() << "config json file write error!";
    }
};

QJsonObject MyConfig::toQJsonObject() const
{
    return QJsonObject::fromVariantHash(this->config_params);
};
