import json

from decouple import config
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, text
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
import requests
from fastapi import HTTPException

# Создаем базовый класс для определения моделей
Base = declarative_base()


# Определяем модель для таблицы 'category'
class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    clues_count = Column(Integer)


# Определяем модель для таблицы 'jservice'
class JService(Base):
    __tablename__ = 'jservice'
    jservice_pk = Column(Integer, primary_key=True)
    id = Column(Integer)
    answer = Column(String)
    question = Column(String)
    value = Column(Integer)
    airdate = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    category_id = Column(Integer, ForeignKey('category.id'))
    game_id = Column(Integer)
    invalid_count = Column(Integer)
    category = relationship("Category")


class Executor:
    def __init__(self):
        self.db_url = config('DB_URL')
        self.engine = create_engine(
            self.db_url,
            poolclass=QueuePool,
            max_overflow=10,
            pool_size=10,
            pool_reset_on_return=None,
            isolation_level="AUTOCOMMIT",
            # echo_pool="debug"
        )
        self.Session = sessionmaker(bind=self.engine)

    def check_category_id_exists(self, category_id: int):
        with self.Session() as session:
            try:
                result = session.query(Category).filter_by(id=category_id).first()
                if result:
                    session.commit()
                    session.close()
                    self.engine.dispose()
                    return True
                else:
                    session.commit()
                    session.close()
                    self.engine.dispose()
                    return False
            except Exception as ex:
                print(ex)
                session.commit()
                session.close()
                self.engine.dispose()
                return False

    def check_jservice_id_exists(self, jservice_id: int):
        with self.Session() as session:
            try:
                result = session.query(JService).filter_by(id=jservice_id).first()
                if result:
                    return True
                else:
                    return False
            except Exception as ex:
                print(ex)
                return False

    def add_new_element_category(
            self,
            category_id: int,
            title: str,
            created_at: str,
            updated_at: str,
            clues_count: int
    ):
        with self.Session() as session:
            new_category = Category(
                id=category_id,
                title=title,
                created_at=created_at,
                updated_at=updated_at,
                clues_count=clues_count
            )
            session.add(new_category)
            session.commit()
            self.engine.dispose()
            return 0

    def add_new_element_jservice(
            self,
            jservice_id: int,
            answer: str,
            question: str,
            value: int,
            airdate: str,
            created_at: str,
            updated_at: str,
            category_id: int,
            game_id: int,
            invalid_count: int
    ):
        with self.Session() as session:
            new_jservice = JService(
                id=jservice_id,
                answer=answer,
                question=question,
                value=value,
                airdate=airdate,
                created_at=created_at,
                updated_at=updated_at,
                category_id=category_id,
                game_id=game_id,
                invalid_count=invalid_count
            )
            session.add(new_jservice)
            session.commit()
            self.engine.dispose()
            return 0

    def get_last_question(self):
        with self.Session() as session:
            select_lv = '''
                SELECT last_value FROM jservice_pk_seq;
            '''
            query_result = session.execute(text(select_lv)).scalar()
            select_lq = f'''
                SELECT question
                FROM public.jservice
                WHERE jservice_pk = {int(query_result) - 1};
            '''
            result = session.execute(text(select_lq))
        return result


def fetch_questions(num: int):
    url = config('JSERVICE_API_URL')
    response = requests.get(url + str(num))
    if response.status_code == 200:
        data = response.json()
        db_worker(num, data)
        return get_last_question()
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch questions")


def db_worker(num, data):
    counter = 0
    executor = Executor()
    for i in range(num):
        category = data[i]['category']
        category_id = category['id']
        title = category['title']
        created_at = category['created_at']
        updated_at = category['updated_at']
        clues_count = category['clues_count']
        exist_category = executor.check_category_id_exists(category_id=category_id)
        if exist_category:
            pass
        else:
            executor.add_new_element_category(
                category_id=category_id,
                title=title,
                created_at=created_at,
                updated_at=updated_at,
                clues_count=clues_count
            )
        jservice_id = data[i]['id']
        answer = data[i]['answer']
        question = data[i]['question']
        value = data[i]['value']
        airdate = data[i]['airdate']
        created_at = data[i]['created_at']
        updated_at = data[i]['updated_at']
        category_id = data[i]['category_id']
        game_id = data[i]['game_id']
        invalid_count = data[i]['invalid_count']
        exist_jservice = executor.check_jservice_id_exists(jservice_id=jservice_id)
        if exist_jservice:
            counter += 1
        else:
            executor.add_new_element_jservice(
                jservice_id=jservice_id,
                answer=answer,
                question=question,
                value=value,
                airdate=airdate,
                created_at=created_at,
                updated_at=updated_at,
                category_id=category_id,
                game_id=game_id,
                invalid_count=invalid_count
            )
        if counter > 0:
            fetch_questions(num=counter)
        else:
            return 0


def get_last_question():
    executor = Executor()
    lq = executor.get_last_question().scalar()
    if lq:
        return lq
    else:
        return "Empty object"
