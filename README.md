# AWS_Assignmnet

Deployment Steps -:

[A] - Creation of IAM role ->
 1 - Create an IAM Role for lambda function.
 2 - Give full admin permisiion for SES and EC2.
 3 - Subscribe and verfiy the email address for SES notification.
 
[B] - Creation of event rule in event bridge ->
 1 - To trigger ec2 events for lambda.
 
[C]- Creation of lambda function ->
 1 - Create lambda function and attach IAM role created above. 
 2 - Select Programming language ( here I've used python 3.9 ).
 3 - Upload the python script in zip format.
 4 - Launch ec2 instances with tags and test lambda function by creating a test event.

The objective of the code is to check every hour those instances which does not have either name or environment tag. If it finds instances which have missing aforementioned tags and and notify the user by using createdBy tag to send a email to tag the instance. Once 6hourse have passed after notifying, function should send a email to notfying the termination of instance.

Approach -> 
1. I have used boto3 which is an AWS sdk to interact with aws.
2. Initiating with fetching all the running ec2 instances and storing it in a dictionary for future use.
3. Now, fetching tag details for each instance and storing it temporarily in a dictionary.
4. Declared a "count" and "mising_tags" variable which tracks the count of missing tags and will append the tag in the missing_tag for future use while sending email.
5. The logic is now to check the count - that is whether any tag is missing or not.
6. If missing that is count not 0. It will check whether TerminateOn tag is present in the instance or not -:
 a. If not present(that means checking the instance for the first time) then it'll go in else part and create a tag TerminateOn and initialize it with current time + 6hours from that , so that we can use it   to send an email.
 b. If present (that means have already checked it prior), then it will check terminate_protection whether it is on or off.
    If on, then it'll disable terminate_protection.
    After all this,  lambda function will terminate the instance using the instance id which have missing tags and notify using the email with required details.
