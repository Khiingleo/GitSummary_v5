from flask import Blueprint
from flask import request, render_template, url_for, flash, redirect
from flask_login import current_user
from gitsummary.models import SavedRepository
import os
import requests
from dotenv import load_dotenv


main = Blueprint('main', __name__)

load_dotenv()

@main.route('/home')
@main.route('/', strict_slashes=False)
def landing():
    """The home page of the gitsummary test version 2"""
    try:
        return render_template('landing.html')
    except Exception as e:
        return render_template('search.html', error='unexpected error occured')

@main.route('/search')
def homepage():
    try:
        return render_template('search.html')
    except Exception as e:
        return render_template('search.html', error=f"an unexcpected error occured {e}")


@main.route('/about', strict_slashes=False)
def about():
    """about page for gitsummary"""
    return render_template("about.html")


@main.route('/error', strict_slashes=False, methods=['GET', 'POST'])
def error():
    """search type error"""
    flash("Please select a search type", 'danger')
    return render_template("error.html")

@main.route('/users', strict_slashes=False, methods=['GET', 'POST'])
def search_user():
    """get github user info"""
    if request.method == 'POST':
        username = request.form.get('search_query')
        search_type = request.form.get('search_type')
        if not username:
            return render_template('user.html', error="Please enter a github username")
        if not search_type:
            return redirect(url_for('main.error'))
        github_api = f"https://api.github.com/users/{username}"
        my_token = os.getenv('GIT_TOKEN')
        
        headers = {'Authorization': f'token {my_token}'}
        
        try:
            user_response = requests.get(github_api, headers=headers)
            if user_response.status_code != 200:
                return render_template('user.html', error="couldn't find user profile or user doesn't exist")
            else:
                user_data = user_response.json()
            
            repos_response = requests.get(github_api + '/repos', headers=headers)
            if repos_response.status_code != 200:
                return render_template('user.html', error="couldn't fetch user repositories")
            else:
                repos_data = repos_response.json()
            
            frequently_committed_repos = sorted(
                repos_data,
                key=lambda x: (x['stargazers_count'], x['updated_at']),
                reverse=True
            )[:5]
            
            language_stats = {}
            for repo in repos_data:
                if repo['language']:
                    language = repo['language']
                    if language in language_stats:
                        language_stats[language]+= 1
                    else:
                        language_stats[language] = 1
            most_used_languages = [{'language': lang, 'count': count} for lang, count in language_stats.items()]
            
            user_data['frequently_committed_repos'] = frequently_committed_repos
            user_data['most_used_languages'] = most_used_languages
            
            return render_template('user.html', user_data=user_data, repos_data=repos_data, username=username)
        except Exception as e:
            print(f"an unexpected error occured {e}")
            return render_template('user.html', title='github_user', error="an unexpected error occurred")
    else:
        return render_template("user.html", error="Invalid request")


@main.route('/repos', strict_slashes=False, methods=['GET', 'POST'])
def search_repos():
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        if search_query:
            args = request.form.get('search_query').split(' ')
            if len(args) >= 2:
                username = args[0]
                repository = args[1]

                github_api = f"https://api.github.com/repos/{username}/{repository}"
                my_token = os.getenv('GIT_TOKEN')
                headers = {"Authorization": f"token {my_token}"}

                try:
                    repo_response = requests.get(github_api, headers=headers)
                    if repo_response.status_code != 200:
                        return render_template("repos.html", error="couldn't find repository or repository doesn't exist")
                    else:
                        searched_data = repo_response.json()
                    
                    repo_contents = requests.get(github_api + '/contents', headers=headers)
                    if repo_contents.status_code != 200:
                        return render_template("repos.html", error="could not get repository contents")
                    else:
                        content_data = repo_contents.json()

                    if current_user.is_authenticated:
                        current_url = searched_data["html_url"]
                        is_saved = SavedRepository.query.filter_by(repository_url=current_url).first()
                    else:
                        is_saved = None        
                    return render_template("repos.html", title='github_repo',
                                           content_data=content_data, searched_data=searched_data,
                                           username=username, repository=repository, is_saved=is_saved)
                except Exception as e:
                    exception_error = f"an unexpected error occured {e}"
                    print(exception_error)
                    return render_template("repos.html", error=exception_error)
            else:
                flash("please enter a username and repository name (e.g 'Johnny' 'Github tutorial')", 'danger')
                return render_template("repos.html")
        else:
            return render_template("repos.html")
    else:
        username = request.args.get('username')
        repository = request.args.get('repository')

        if username and repository:
            github_api = f"https://api.github.com/repos/{username}/{repository}"
            my_token = os.getenv('GIT_TOKEN')
            headers = {"Authorization": f"token {my_token}"}

            try:
                repo_response = requests.get(github_api, headers=headers)
                if repo_response.status_code != 200:
                    return render_template("repos.html", error="couldn't find repository or repository doesn't exist")
                else:
                    searched_data = repo_response.json()
                
                repo_contents = requests.get(github_api + '/contents', headers=headers)
                if repo_contents.status_code != 200:
                    return render_template("repos.html", error="could not get repository contents")
                else:
                    content_data = repo_contents.json()

                if current_user.is_authenticated:
                    current_url = searched_data["html_url"]
                    is_saved = SavedRepository.query.filter_by(repository_url=current_url).first()
                else:
                    is_saved = None        
                return render_template("repos.html", title='github_repo',
                                       content_data=content_data, searched_data=searched_data,
                                       username=username, repository=repository, is_saved=is_saved)
            except Exception as e:
                exception_error = f"an unexpected error occured {e}"
                print(exception_error)
                return render_template("repos.html", error=exception_error)
        else:
            return render_template("repos.html")