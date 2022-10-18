from typing import List

from sqlalchemy.orm import sessionmaker

from models_table import Expenses, engine


class ExpensesQuery:
    session = sessionmaker(bind=engine)
    session = session()

    def get_all_data(self) -> List[tuple]:
        """Получение всех данных из таблицы.

        Return:
             List[tuple]: Все данные таблицы.
        """

        all_data = self.session.query(Expenses).all()
        return [row.serialize for row in all_data]

    def get_data_to_id(self, line_id: int) -> tuple:
        """Получение значений из таблицы по заданному id.

        Args:
            line_id: id строки в таблице.

        Return:
            List[tuple]: Данные строки из таблицы по заданному id.
        """
        return (
            self.session.query(Expenses).filter(Expenses.id == line_id).one().serialize
        )

    def add_line(
        self, rubles: float, dollars: float, waste_or_income: str, description: str
    ) -> None:
        """Добавление новой строки в таблицу.

        Args:
            rubles: значение суммы в рублях.
            dollars: значение суммы в долларах.
            waste_or_income: вид транзакции (расход/доход).
            description: описание транзакции.
        """
        query = Expenses(
            rubles=rubles,
            dollars=dollars,
            waste_or_income=waste_or_income,
            description=description,
        )
        self.session.add(query)
        self.session.commit()

    def delete_line_to_id(self, line_id: int) -> None:
        """Удаление строки в таблице по заданному id.

        Args:
            line_id: id строки в таблице.
        """
        del_record = self.session.query(Expenses).filter(Expenses.id == line_id).one()
        self.session.delete(del_record)
        self.session.commit()

    def delete_all_lines(self) -> None:
        """Удаление всех данных таблицы."""
        self.session.query(Expenses).delete(synchronize_session="fetch")
        self.session.commit()

    def update_line(
        self,
        rubles: float,
        waste_or_income: str,
        description: str,
        dollars: float,
        line_id: int,
    ) -> None:
        """Обновление данных строки в таблице.

        Args:
            rubles: рубли.
            waste_or_income: расход или доход.
            description: описание.
            dollars: доллары.
            line_id: id строки в таблице.

        """
        self.session.query(Expenses).filter(Expenses.id == line_id).update(
            {
                "rubles": rubles,
                "waste_or_income": waste_or_income,
                "description": description,
                "dollars": dollars,
            },
            synchronize_session="fetch",
        )

        self.session.commit()


exp_query = ExpensesQuery()
