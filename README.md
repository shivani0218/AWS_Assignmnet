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

