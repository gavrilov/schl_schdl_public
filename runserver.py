from app import create_app


app = create_app('C:/Projects/schl_schdl/config_dev.py')


if __name__ == '__main__':
    app.run()