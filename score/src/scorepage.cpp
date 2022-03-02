#include "scorepage.h"
#include "ui_scorepage.h"
#include <QKeyEvent>
#include <QPainter>

ScorePage::ScorePage(QWidget *parent) : QMainWindow(parent),
                                        ui(new Ui::ScorePage)
{
    ui->setupUi(this);
    this->ui->edit_cur_img->setReadOnly(true);
    init_connections();
}

void ScorePage::init_connections()
{
    connect(ui->btn_confirm_score, SIGNAL(clicked()), this, SLOT(on_btn_confirm_score_clicked()));
    connect(ui->slider_score, SIGNAL(valueChanged(int)), this, SLOT(slider_score_value_changed(int)));
}

void ScorePage::begin_score()
{
    this->setWindowFlags(Qt::FramelessWindowHint | Qt::WindowStaysOnTopHint);
    this->show();
}

void ScorePage::set_edit_content(QString cur_img,QString cur_score){
	this->ui->edit_cur_img->setText(cur_img);
    ui->edit_cur_score->setText(cur_score);
    ui->slider_score->setValue(cur_score.toInt());
}

void ScorePage::slider_score_value_changed(int value)
{
    ui->edit_cur_score->setText(QString::number(value));
    this->update();
}

void ScorePage::keyPressEvent(QKeyEvent *event)
{
    if (event->key() == Qt::Key_Up)
    {
        int value = ui->slider_score->value();
        ui->slider_score->setValue(value + 1);
    }
    if (event->key() == Qt::Key_Down)
    {
        int value = ui->slider_score->value();
        ui->slider_score->setValue(value - 1);
    }
    if (event->key() == Qt::Key_Control)
    {
        this->on_btn_confirm_score_clicked();
        this->update();
    }
    if (event->key() == Qt::Key_Enter||event->key() == Qt::Key_Return){
        this->on_btn_confirm_score_clicked();
        this->update();
    }
};

void ScorePage::on_btn_confirm_score_clicked()
{
    int score = ui->slider_score->value();
    emit submit_score(score);
};

void ScorePage::paintEvent(QPaintEvent *event)
{
    QWidget::paintEvent(event);
    int num = ui->slider_score->value();
    if (num >= 0 && num <= 20)
    {
        ui->slider_score->setStyleSheet(QString::fromUtf8("QSlider::add-page:vertical {background-color:"
                                                          "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ff8800, stop:1 #ff0000);}\n"
                                                          "QSlider::sub-page:vertical {background-color: rgb(220,220,220);}\n"
                                                          "QSlider::groove:vertical {background:transparent;}\n"
                                                          "QSlider::handle:vertical {height: 25px;background: rgb(255, 255, 255);}"));
    }
    else if (num >= 20 && num < 40)
    {
        ui->slider_score->setStyleSheet(QString::fromUtf8("QSlider::add-page:vertical {background-color:"
                                                          "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffff00, stop:1 #ff8800);}\n"
                                                          "QSlider::sub-page:vertical {background-color: rgb(220,220,220);}\n"
                                                          "QSlider::groove:vertical {background:transparent;}\n"
                                                          "QSlider::handle:vertical {height: 25px;background: rgb(255, 255, 255);}"));
    }
    else if (num >= 40 && num < 60)
    {
        ui->slider_score->setStyleSheet(QString::fromUtf8("QSlider::add-page:vertical {background-color:"
                                                          "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #bbff66, stop:1 #ffff00);}\n"
                                                          "QSlider::sub-page:vertical {background-color: rgb(220,220,220);}\n"
                                                          "QSlider::groove:vertical {background:transparent;}\n"
                                                          "QSlider::handle:vertical {height: 25px;background: rgb(255, 255, 255);}"));
    }
    else if (num >= 60 && num < 80)
    {
        ui->slider_score->setStyleSheet(QString::fromUtf8("QSlider::add-page:vertical {background-color:"
                                                          "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #88ff44, stop:1 #bbff66);}\n"
                                                          "QSlider::sub-page:vertical {background-color: rgb(220,220,220);}\n"
                                                          "QSlider::groove:vertical {background:transparent;}\n"
                                                          "QSlider::handle:vertical {height: 25px;background: rgb(255, 255, 255);}"));
    }
    else
    {
        ui->slider_score->setStyleSheet(QString::fromUtf8("QSlider::add-page:vertical {background-color:"
                                                          "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #00ff77, stop:1 #88ff44);}\n"
                                                          "QSlider::sub-page:vertical {background-color: rgb(220,220,220);}\n"
                                                          "QSlider::groove:vertical {background:transparent;}\n"
                                                          "QSlider::handle:vertical {height: 25px;background: rgb(255, 255, 255);}"));
    }
};

ScorePage::~ScorePage()
{
    delete ui;
}
