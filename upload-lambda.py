import boto3
from botocore.client import Config
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):
    
    sns = boto3.resource('sns') 
    topic = sns.Topic('arn:aws:sns:us-east-1:366391210774:deployRMSWebsiteTopic')
    
    location = {
        "bucketName": "build.ryanmattscott.com",
        "objectKey": 'websitebuild.zip'
    }
    
    try:
        job = event.get("CodePipeline.job")
        if job:
            for artifact in job["data"]["inputArtifacts"]:
                if artifact["name"] == "BuildArtifact":
                    location = artifact["location"]["s3Location"]
        
        print "building website from " + str(location)
        
        s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
        website_bucket = s3.Bucket('ryanmattscott.com')
        build_bucket = s3.Bucket(location["bucketName"])
    
        build_zip = StringIO.StringIO()
        build_bucket.download_fileobj(location["objectKey"], build_zip)
    
        with zipfile.ZipFile(build_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                website_bucket.upload_fileobj(obj, nm,
                ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                website_bucket.Object(nm).Acl().put(ACL='public-read')
    
        topic.publish(Subject='Publish Lambda', Message='Website successfully Deployed')
        if job:
            codepipeline = boto3.client('codepipeline')
            codepipeline.put_job_success_result(jobId=job["id"])
    except:
        topic.publish(Subject='Publish Lambda', Message="Website deployment error")
        raise
    return 'hi from Lambda'