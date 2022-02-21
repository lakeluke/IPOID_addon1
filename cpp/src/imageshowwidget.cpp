#include "imageshowwidget.h"
#include <QLayout>

ImageShowWidget::ImageShowWidget(QWidget *parent)
    : QWidget{parent}
{
    this->image_layout = new QGridLayout(this);
    this->image_display = new QLabel(this);

};

void ImageShowWidget::init_ui(){
    this->image_layout->setObjectName("image_layout");
    this->image_layout->setContentsMargins(0, 0, 0, 0);
    this->image_layout->setSpacing(5);
    this->image_display->setLineWidth(0);
    this->image_display->setAlignment(Qt::AlignCenter);
    this->image_display->setObjectName("image_display");
    this->image_display->setStyleSheet("background-color:#808080");
    this->image_layout->addWidget(this->image_display);

};
void ImageShowWidget::init_timer(){

};
void ImageShowWidget::init_connections(){

};
void ImageShowWidget::load_config(){

};
void ImageShowWidget::load_images(){

};
void ImageShowWidget::subscribe_eye_data(){

};
void ImageShowWidget::save_eye_data(){

};

void ImageShowWidget::begin_test(const QString& participant_id){

};
void ImageShowWidget::continue_test(const QString& participant_id){

};
void ImageShowWidget::pause(const QString& str){

};


void ImageShowWidget::do_timer_timeout(){

};
void ImageShowWidget::do_error_detection(){

};

void ImageShowWidget::keyReleaseEvent(QKeyEvent*){

};
