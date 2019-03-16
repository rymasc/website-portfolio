import boto3
from botocore.client import Config
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):
    
    sns = boto3.resource('sns') 
    topic = sns.Topic('arn:aws:sns:us-east-1:366391210774:deployRMSWebsiteTopic')
    
    try:
        s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
        website_bucket = s3.Bucket('ryanmattscott.com')
        build_bucket = s3.Bucket('build.ryanmattscott.com')
    
        build_zip = StringIO.StringIO()
        build_bucket.download_fileobj('websitebuild.zip', build_zip)
    
        with zipfile.ZipFile(build_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                website_bucket.upload_fileobj(obj, nm,
                ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                website_bucket.Object(nm).Acl().put(ACL='public-read')
    
        topic.publish(Subject='Publish Lambda', Message='Website successfully Deployed')
    except:
        topic.publish(Subject='Publish Lambda', Message="Website deployment error")
        raise
    return 'hi from Lambda'