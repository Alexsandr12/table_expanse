from typing import Union

from sqlalchemy.exc import NoResultFound
from flask_bootstrap import Bootstrap
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.wrappers.response import Response

from config import ERROR_PAGE, REDIRECT_PAGE
from sql_handler import exp_query
from logger import logger_expenses
from utils import get_dollar_value


app = Flask(__name__)
Bootstrap(app)


@app.route("/", methods=["GET"])
def index() -> str:
    """Основной route приложения.

    Returns:
        str: html страницы.
    """
    try:
        all_data = exp_query.get_all_data()
        return render_template("index.html", data=all_data)
    except Exception as e:
        logger_expenses.error(f"Ошибка: {e}", exc_info=True)
        return render_template(ERROR_PAGE, reason="unknown_error")


@app.route("/add_data", methods=["POST"])
def add_data() -> Union[Response, str]:
    """Добавление строки с данными в таблицу.

    Returns:
        Union[Response, str]: редирект на основную html или html-страница.
    """
    form = request.form
    try:
        rubles = float(form["rub"])
        waste_or_income = form["w/i"].strip() if form["w/i"].strip() else None
        description = form["desc"].strip() if form["desc"].strip() else None
        dollars = round(rubles / get_dollar_value(), 2)
        if not waste_or_income or not description:
            raise ValueError
    except ValueError as e:
        logger_expenses.error(f"Ошибка: {e}", exc_info=True)
        return render_template(ERROR_PAGE)

    try:
        exp_query.add_line(rubles, dollars, waste_or_income, description)
        logger_expenses.debug(
            "Добавлена строка с данными: "
            f"rubles = {rubles}, dollars = {dollars}, "
            f"w/i = {waste_or_income}, description = {description}"
        )
        return redirect(url_for(REDIRECT_PAGE))
    except Exception as e:
        logger_expenses.error(f"Ошибка: {e}", exc_info=True)
        return render_template(ERROR_PAGE, reason="unknown_error")


@app.route("/delete_data", methods=["POST"])
def delete_data() -> Union[Response, str]:
    """Удаление строки с данными в таблице.

    Returns:
        Union[Response, str]: редирект на основную html или html-страница.
    """
    try:
        line_id = int(request.form["id"])
    except ValueError as e:
        logger_expenses.error(f"Ошибка: {e}", exc_info=True)
        return render_template(ERROR_PAGE)

    try:
        delete_line = exp_query.get_data_to_id(line_id)
    except NoResultFound as e:
        logger_expenses.error(f"Ошибка: {e}", exc_info=True)
        return render_template(ERROR_PAGE, reason="invalid_index")

    logger_expenses.debug(
        f"Запрос на удаление строки с id {line_id}, данные строки: "
        f"rubles = {delete_line[1]}, dollars = {delete_line[2]}, date = {delete_line[3]}, "
        f"w/i = {delete_line[4]}, description = {delete_line[5]}"
    )

    try:
        exp_query.delete_line_to_id(line_id)
        logger_expenses.debug(f"Удалена строка с id {line_id}")
        return redirect(url_for(REDIRECT_PAGE))
    except Exception as e:
        logger_expenses.error(f"Ошибка: {e}", exc_info=True)
        return render_template(ERROR_PAGE, reason="unknown_error")


@app.route("/delete_all_data", methods=["POST"])
def delete_all_data() -> Union[Response, str]:
    """Удаление всех строк в таблице.

    Returns:
        Union[Response, str]: редирект на основную html или html-страница.
    """
    try:
        exp_query.delete_all_lines()
        logger_expenses.debug("Все данные удалены")
        return redirect(url_for(REDIRECT_PAGE))
    except Exception as e:
        logger_expenses.error(f"Ошибка: {e}", exc_info=True)
        return render_template(ERROR_PAGE, reason="unknown_error")


@app.route("/update_data", methods=["POST"])
def update_data() -> Union[Response, str]:
    """Route для изменения строки с данными в таблицу.

    Returns:
        Union[Response, str]: редирект на основную html или html-страница.
    """
    try:
        line_id = int(request.form["id"])
    except ValueError as e:
        logger_expenses.error(f"Ошибка: {e}", exc_info=True)
        return render_template(ERROR_PAGE)

    try:
        line_to_id = exp_query.get_data_to_id(line_id)
    except NoResultFound as e:
        logger_expenses.error(f"Ошибка: {e}", exc_info=True)
        return render_template(ERROR_PAGE, reason="invalid_index")

    logger_expenses.debug(
        f"Запрос на изменение данных в строке с id {line_id}: "
        f"rubles = {line_to_id[1]}, dollars = {line_to_id[2]}, date = {line_to_id[3]}, "
        f"w/i = {line_to_id[4]}, description = {line_to_id[5]}"
    )

    form = request.form

    try:
        rubles = float(form["rub"]) if form["rub"] else line_to_id[1]
        waste_or_income = form["w/i"] if form["w/i"].strip() else line_to_id[4]
        description = form["desc"] if form["desc"].strip() else line_to_id[5]
        dollars = round(rubles / get_dollar_value(), 2)
    except ValueError as e:
        logger_expenses.error(f"Ошибка: {e}", exc_info=True)
        return render_template(ERROR_PAGE)

    try:
        exp_query.update_line(rubles, waste_or_income, description, dollars, line_id)
        line_to_id = exp_query.get_data_to_id(line_id)
        logger_expenses.debug(
            "Данные изменены на: "
            f"rubles = {line_to_id[1]}, dollars = {line_to_id[2]}, date = {line_to_id[3]}, "
            f"w/i = {line_to_id[4]}, description = {line_to_id[5]}"
        )
        return redirect(url_for(REDIRECT_PAGE))
    except Exception as e:
        logger_expenses.error(f"Ошибка: {e}", exc_info=True)
        return render_template(ERROR_PAGE, reason="unknown_error")


if __name__ == "__main__":
    app.run()
