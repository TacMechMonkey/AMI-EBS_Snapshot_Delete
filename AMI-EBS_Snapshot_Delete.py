import boto3
region = 'ap-southeast-2'
ec = boto3.client('ec2', region)
ec2 = boto3.resource('ec2', region)
images = ec2.images.filter(Owners=["self"])



def ami_snap_DELETE():

    imagesList = ['ami-11111111111111', 'ami-222222222222222']

    print('Images marked for deregistration: ',imagesList)

    if imagesList != []:

        myAccount = boto3.client('sts').get_caller_identity()['Account']
        snapshots = ec.describe_snapshots(MaxResults=1000, OwnerIds=[myAccount])['Snapshots']

        for image in imagesList:
            print("deregistering image %s" % image)
            amiResponse = ec.deregister_image(
                DryRun=False,
                ImageId=image,
            )

            for snapshot in snapshots:
                if snapshot['Description'].find(image) > 0:
                    snap = ec.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
                    print("Deleting snapshot " + snapshot['SnapshotId'])

    else:
        print("No images found.")

ami_snap_DELETE()
