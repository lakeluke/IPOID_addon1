#include "myconfig.h"
#include <QFileInfo>
#include <QJsonDocument>
#include <QJsonParseError>

MyConfig::MyConfig()
{
    this->default_init();
};

MyConfig::MyConfig(const QString config_file_str){
    QFile config_file(config_file_str);
    QFileInfo config_file_info(config_file);
    QString suffix = config_file_info.suffix();
    config_file.open(QIODevice::ReadOnly);
    QByteArray data = config_file.readAll();
    config_file.close();
    if(suffix == "json"){
        QJsonParseError parseError;
        QJsonDocument doc = QJsonDocument::fromJson(data,&parseError);
        if(parseError.error == QJsonParseError::NoError){
            qDebug()<<QStringLiteral("配置错误");
            return;
        }
        QJsonObject obj=doc.object();
        new (this)MyConfig(obj);
    }
};

MyConfig::MyConfig(const QJsonObject config_in_qjson){
    this->config_params = config_in_qjson.toVariantHash();
    config_source.append("QJsonObject");
    this->load_eyetracker();
};

MyConfig::MyConfig(const MyConfig& other){
    if(this==&other){
        return;
    }
    config_params = other.config_params;
    config_source = other.config_source;
    eyetracker_wrapper = new EyeTrackerWrapper(*other.eyetracker_wrapper);
};

MyConfig::~MyConfig(){
    if(this->eyetracker_wrapper)
        delete this->eyetracker_wrapper;
};

void MyConfig::default_init(){
    QString json_config_str = "{\"eyetracker\": {\"frequency\": 60,\"calibration_point_number\": 9},"
                              "\"database\": {\"path\": \"./imgdb\"},\"data\": {\"path\": \"./outdata\"},"
                              "\"log\": {\"path\": \"./log\"},\"image_show\": {\"last_time\": 10,\"time_interval\": 3},"
                              "\"mode\": {\"debug\": false}}";
    QJsonParseError parseError;
    QJsonDocument json_doc = QJsonDocument::fromJson(json_config_str.toUtf8(),&parseError);
    QJsonObject json_config = json_doc.object();
    config_params = json_config.toVariantHash();
    config_source = "default";
    this->load_eyetracker();
};

void MyConfig::load_eyetracker(const QString& address){
    eyetracker_wrapper = new EyeTrackerWrapper(address);
};

void MyConfig::set_value(const QString& key,const QVariant value){
    config_params[key] = value;
};

QVariant MyConfig::get_value(const QString& key,const QVariant default_value) const{
    QStringList skeys = key.split('/');
    if(skeys.size()==1){
        if(config_params.contains(key))
            return config_params[key];
        else
            return default_value;
    }
    QVariant value = this->config_params[skeys[0]];
    int idx = 1;
    while(idx<skeys.size()-1){
        if(value.toHash().contains(skeys[idx])){
            value = value.toHash()[skeys[idx]];
            idx++;
        }else
            return default_value;
    }
    return value.toHash()[skeys[idx]];
};

EyeTrackerWrapper* MyConfig::get_eyetracker_wrapper() const{
    return this->eyetracker_wrapper;
}

void MyConfig::dump(const QString& fileName)const{
    QFile file(fileName);
    QJsonObject obj = QJsonObject::fromVariantHash(this->config_params);
    QJsonDocument doc(obj);
    bool ok = file.open(QIODevice::WriteOnly);
    if(ok){
        file.write(doc.toJson());
        file.close();
    }else{
        qDebug()<<"config json file write error!";
    }
};

QJsonObject MyConfig::toQJsonObject()const{
    return QJsonObject::fromVariantHash(config_params);
};




