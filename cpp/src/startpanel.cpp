#include "startpanel.h"
#include "ui_startpanel.h"

StartPanel::StartPanel(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::StartPanel),
    eye_show(new EyePosShow(ui->widget_eyepos)),
    timer(new QTimer())
{
    ui->setupUi(this);
}

StartPanel::~StartPanel()
{
    delete ui;
    delete eye_show;
    delete timer;
}
