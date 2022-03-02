#ifndef SCOREPAGE_H
#define SCOREPAGE_H

#include <QMainWindow>

namespace Ui
{
    class ScorePage;
}

class ScorePage : public QMainWindow
{
    Q_OBJECT

public:
    explicit ScorePage(QWidget *parent = nullptr);
    ~ScorePage();
    Ui::ScorePage *ui;
    virtual void keyPressEvent(QKeyEvent*) override;

signals:
    void submit_score(int);

public slots:
    void begin_score();
    void set_edit_content(QString,QString);

private slots:
    void on_btn_confirm_score_clicked();
    void slider_score_value_changed(int value);

private:
    void init_connections();
    virtual void paintEvent(QPaintEvent*) override;
};

#endif // SCOREPAGE_H
