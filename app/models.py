# Global models
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Table, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

recipe_ingredient_association = Table('recipe_ingredient', Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id')),
    Column('ingredient_id', Integer, ForeignKey('ingredients.id'))
)

user_saved_recipes = Table('user_saved_recipes', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('recipe_id', Integer, ForeignKey('recipes.id'))
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(100))
    password = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    recipes = relationship('Recipe', back_populates='author')
    ingredients = relationship('Ingredient', back_populates='author')
    preferences = relationship('UserPreference', back_populates='user')
    saved_recipes = relationship('Recipe', secondary=user_saved_recipes, back_populates='saved_by_users')

    def __repr__(self):
        return f'<User(id={self.id}, username={self.username}, email={self.email}, full_name={self.full_name})>'

class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    author = relationship('User', back_populates='ingredients')
    recipes = relationship('Recipe', secondary=recipe_ingredient_association, back_populates='ingredients')

    def __repr__(self):
        return f'<Ingredient(id={self.id}, name={self.name})>'

class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    instructions = Column(Text, nullable=False)
    image_name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    low_carb = Column(Boolean, default=False)
    gluten_free = Column(Boolean, default=False)

    author = relationship('User', back_populates='recipes')
    ingredients = relationship('Ingredient', secondary=recipe_ingredient_association, back_populates='recipes')
    saved_by_users = relationship('User', secondary=user_saved_recipes, back_populates='saved_recipes')

    def __repr__(self):
        return f'<Recipe(id={self.id}, title={self.title}, author_id={self.author_id})>'

class UserPreference(Base):
    __tablename__ = 'user_preferences'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    preference_type = Column(String(50), nullable=False)  # 'allergy', 'like', 'dislike'
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), nullable=False)

    user = relationship('User', back_populates='preferences')
    ingredient = relationship('Ingredient')