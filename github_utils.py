import os
from github import Github
from datetime import datetime

def create_pr(topic_name, sa_name, topic_code, sa_code, acl_code, metadata):
    g = Github(os.getenv("GITHUB_TOKEN"))
    repo = g.get_repo(os.getenv("GITHUB_REPO"))
    branch_name = f'{os.getenv("GITHUB_BRANCH_PREFIX")}-{topic_name}-{datetime.now().strftime("%Y%m%d%H%M")}'

    source = repo.get_branch(os.getenv("MAIN_BRANCH"))
    repo.create_git_ref(ref=f'refs/heads/{branch_name}', sha=source.commit.sha)

    repo.create_file(f"topics/{topic_name}.tf", f"Add topic {topic_name}", topic_code, branch_name)
    repo.create_file(f"service_accounts/{sa_name}.tf", f"Add service account {sa_name}", sa_code, branch_name)
    repo.create_file(f"acls/{sa_name}-{topic_name}.tf", f"Add ACLs for {sa_name}", acl_code, branch_name)

    # PR Body
    pr_body = f"""
### Kafka Resource Request

**Topic Name**: `{topic_name}`  
**Service Account**: `{sa_name}`  
**ACL Type**: `{metadata['environment']}`  
**Team**: `{metadata['team']}`  
**Environment**: `{metadata['environment']}`  
**Purpose**:  
{metadata['purpose']}

---

Please review Terraform resources before approving.
"""

    pr = repo.create_pull(
        title=f"Kafka Resource Request: {topic_name}",
        body=pr_body,
        head=branch_name,
        base=os.getenv("MAIN_BRANCH")
    )
    return pr.html_url
