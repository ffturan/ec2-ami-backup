### Create AMI Backups for tagged EC2 Instances
#### AWS Lambda function

If you tag your EC2 instances with Backup:True tag key:value this AWS lambda function will create AMI backup of those EC2 instances.
Run at desired schedule through CloudWatch rules. 

### Requirements
Lambda function will need IAM role with following policies  
	- arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole  
	- EC2 policy for AMI creation  
Please set your environment variables matching your EC instance tags.
![Env Vars](/img.png)

### Output
```shell
Sample output:  
ami-023f8b3d457ecabcd has been created with name test-server-01-i-085c25913743aabcd-2020-10-19

```
