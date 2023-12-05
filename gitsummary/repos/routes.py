from flask import request, render_template, url_for, flash, redirect, Blueprint
from flask_login import current_user, login_required
from gitsummary.models import SavedRepository
from gitsummary import db
import os
from dotenv import load_dotenv
import requests


repos = Blueprint('repos', __name__)

load_dotenv()

@repos.route("/save_repository", strict_slashes=False, methods=['GET', 'POST'])
@login_required
def save_repository():
    """save repository"""
    repository_name = request.form.get('repository_name')
    repository_url = request.form.get('repository_url')
    url = request.form.get("url")

    saved_repo = SavedRepository(repository_name=repository_name,
                                 repository_url=repository_url, url=url, user_id=current_user.id)
    db.session.add(saved_repo)
    db.session.commit()

    flash("Repository saved successfully", 'success')
    return redirect(url_for('main.search_repos'))


@repos.route("/saved_repositories", strict_slashes=False)
@login_required
def saved_repositories():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    saved_repos = SavedRepository.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=per_page, error_out=False)
    repo_data_list = []
    for repo in saved_repos:
        git_api = repo.url
        my_token = os.getenv('GIT_TOKEN')
        headers = {"Authorization": f"token {my_token}"}

        try:
            repo_response = requests.get(git_api, headers=headers)
            if repo_response.status_code != 200:
                return render_template('saved_repositories.html',
                                       title="Saved Repository", error="Couldn't get repo info")
            else:
                repo_data = repo_response.json()
                repo_data_list.append(repo_data)
        except Exception as e:
            return render_template('saved_repositories.html',
                                   title="Saved Repository", error=f"An unexpected error occurred: {e}")

    return render_template("saved_repositories.html", saved_repos=saved_repos, repo_data_list=repo_data_list)
    # return render_template("saved_repositories.html", saved_repos=saved_repos)


@repos.route("/view_saved_repository/<int:repo_id>", strict_slashes=False)
@login_required
def view_saved_repository(repo_id):
    saved_repo = SavedRepository.query.get_or_404(repo_id)
    git_api = saved_repo.url
    my_token = os.getenv('GIT_TOKEN')
    headers = {"Authorization": f"token {my_token}"}
    try:
        repo_response = requests.get(git_api, headers=headers)
        if repo_response.status_code != 200:
            return render_template('user_saved_repositories.html', title="Saved Repository", error="couldn't get repo info")
        else:
            repo_data = repo_response.json()
        repo_contents = requests.get(git_api + '/contents', headers=headers)
        if repo_contents.status_code != 200:
            return render_template("user_saved_repositories.html", error="could not get repository contents")
        else:
            content_data = repo_contents.json()
        return render_template("user_saved_repositories.html",
                               title='Saved Repository', saved_repo=saved_repo,
                               content_data=content_data, searched_data=repo_data)
    except Exception as e:
        exception_error = f"an unexpected error occured {e}"
        print(exception_error)
        return render_template("user_saved_repositories.html", error=exception_error)
    # return render_template('user_saved_repositories.html', title="Saved Repository", saved_repo=saved_repo)


@repos.route('/delete_saved_repository/<int:repo_id>', methods=['POST', 'GET'])
@login_required
def delete_saved_repository(repo_id):
    saved_repo = SavedRepository.query.get_or_404(repo_id)
    db.session.delete(saved_repo)
    db.session.commit()

    flash("Repository deleted successfully!", 'success')
    return redirect(url_for('repos.saved_repositories'))