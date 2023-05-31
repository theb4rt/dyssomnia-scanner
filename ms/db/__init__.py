from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
from ms import app
from flask_sqlalchemy import SQLAlchemy, Model as BaseModel


class Model(BaseModel):
    _fillable = list()

    def set_attributes(self, data: dict) -> None:
        for key, value in data.items():
            if key in self._fillable:
                setattr(self, key, value)
            else:
                raise AttributeError(f"Attribute '{key}' does not exist in the model.")

    def update(self, data: dict) -> None:
        self.set_attributes(data)


db = SQLAlchemy(app, model_class=Model)
# compare_type=True is required for comparing types in migrations
migrate = Migrate(app, db, compare_type=True)

seeder = FlaskSeeder()
seeder.init_app(app, db)
