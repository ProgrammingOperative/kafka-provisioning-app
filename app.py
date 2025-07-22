from flask import Flask, request, render_template
from github_utils import create_pr
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

env = Environment(loader=FileSystemLoader('templates'))


@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        topic_name = request.form['topic_name']
        sa_name = request.form['sa_name']
        acl_type = request.form['acl_type']
        team = request.form['team']
        environment = request.form['environment']
        purpose = request.form['purpose']

        topic_code = env.get_template('topic.tf.j2').render(topic_name=topic_name)
        sa_code = env.get_template('service_account.tf.j2').render(sa_name=sa_name)
        acl_code = env.get_template('acl.tf.j2').render(topic_name=topic_name, sa_name=sa_name, acl_type=acl_type)

        pr_url = create_pr(
            topic_name, sa_name, topic_code, sa_code, acl_code,
            metadata={"team": team, "environment": environment, "purpose": purpose}
        )

        return f'<h3>PR Created!</h3><a href="{pr_url}" target="_blank">View PR</a>'
    return render_template('form.html')


if __name__ == '__main__':
    app.run(debug=True)

