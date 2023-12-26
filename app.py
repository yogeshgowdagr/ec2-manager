from flask import Flask, render_template, request, flash
import boto3
from botocore.exceptions import ClientError


app = Flask(__name__)
app.secret_key = 'supersecretkey' 

# This will render a simple form where the user can input the required details.
@app.route('/', methods=['GET', 'POST'])
def index():
    feedback = None
    if request.method == 'POST':
        if 'start' in request.form:
            action = 'start'
        elif 'stop' in request.form:
            action = 'stop'
        else:
            action = None
        
        instance_id = request.form.get('instance_id', '')
        tag_key = request.form.get('tag', '')
        tag_value = request.form.get('tag_value', '')
        region = request.form.get('region', 'us-west-2')
        access_key = request.form.get('access_key', '')
        secret_key = request.form.get('secret_key', '')

        ec2_resource = boto3.resource('ec2', region_name=region,
                                      aws_access_key_id=access_key,
                                      aws_secret_access_key=secret_key)

        # Start or stop the instance based on the action
        if action and (instance_id or (tag_key and tag_value)):
            instances = []
            if instance_id:
                instances.append(instance_id)
            else:
                filters = [{'Name': f'tag:{tag_key}', 'Values': [tag_value]}]
                instances = [instance.id for instance in ec2_resource.instances.filter(Filters=filters)]

        try:
            if action == 'start':
                ec2_resource.instances.filter(InstanceIds=instances).start()
                feedback = f'Start command sent to instances: {", ".join(instances)}.'
            elif action == 'stop':
                ec2_resource.instances.filter(InstanceIds=instances).stop()
                feedback = f'Stop command sent to instances: {", ".join(instances)}.'
            flash(feedback, 'success')
        except ClientError as e:
            # You can print or log the error here to debug or store it for records
            error_msg = f"An error occurred: {e}"
            flash(error_msg, 'error')
        except Exception as e:
            # Catch all other exceptions
            error_msg = f"An unexpected error occurred: {str(e)}"
            flash(error_msg, 'error')

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
