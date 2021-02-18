from flask import jsonify
from data_access.closet_dao import closet_dao
from model.closet_model import Closet


def create_closet(username, closet):
    """
    This function corresponds to a POST request to /api/user/{user_name}/closet/
    with a list of all closets being returned

    :param username:      username of the user to create a closet for
    :param closet:        the closet to create
    :return:              201 on success, 409 if closet exists
    """
    try:
        closet_name = closet.get('name')
        closet = closet_dao.get_by_name(username, closet_name)

        if closet is not None:
            return "Closet with name for this user already exists", 409
        else:
            closet_dao.create_closet(username, closet_name)
            return "Successfully created closet", 201

    except Exception as error:
        return jsonify(error=str(error)), 500


def get_closets(user_name):
    """
    This function corresponds to a GET request for /api/user/{user_name}/closet/
    with a list of all closets being returned

    :param user_name:      username of the user to retrieve from
    :return:               list of user's closets
    """
    return ''


def get_closet(username, closet_name):
    """
    This function corresponds to a GET request for /api/user/{user_name}/closet/{closet_name}
    with the specified closet being returned

    :param user_name:      username of the user to retrieve from
    :param closet_name:    name of the closet to retrieve
    :return:               (200) the user's closet matching with the name, (404) closet not found
    """

    try:
        closet = closet_dao.get_by_name(username, closet_name)

        if closet is not None:
            return jsonify(id=closet.closet_id,
                           name=closet.closet_name)
        else:
            return 'Closet Not Found', 404
    except Exception as error:
        return jsonify(error=str(error)), 500


def delete_closet(username, closet_name):
    """
    This function corresponds to a DELETE request for /api/user/{user_name}/closet/{closet_name}
    with the specified closet being returned

    :param user_name:      username of the user to retrieve from
    :param closet_name:    name of the closet to retrieve
    :return:               (200) the user's closet matching with the name, (404) closet not found
    """

    try:
        closet = closet_dao.get_by_name(username, closet_name)

        if closet is not None:
            closet_dao.delete_closet(closet)
            return jsonify(id=closet.closet_id,
                           name=closet.closet_name)
        else:
            return 'Closet Not Found', 404
    except Exception as error:
        return jsonify(error=str(error)), 500


def get_best_outfit(closet_id):
    """
    This function corresponds to a GET request for /api/closet/{closet_id}/best-outfit
    with a recommended outfit for that closet being returned

    :param closet_id:   id of the closet the user wants recommendations from
    :return:            TODO!
    """
    try:
        outfit_items = closet_dao.recommend_outfit(closet_id)
        return jsonify(outfit_items), 200
    except Exception as error:
        return jsonify(error = str(error)), 500


