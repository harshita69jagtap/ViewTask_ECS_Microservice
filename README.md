This is ViewTask Python Microservice

It contains a dockerfile which is used to create a docker image that is used in

containerDefinition part of ECS TaskDefinition for viewtask ECS service task

This is another frontend facing microservice with which end users communicate 

Therefore it is hosted on an ECS Container EC2 Instance inside an ECS cluster residing in a public subnet

behind a public ALB , This microservice communicates with the backend dbtask microservice via private ALB to retrieve all existing records from the SQLITE database

and display it to the users
