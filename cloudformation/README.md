Procedure involved in B/G deployment as below:

1) Launch Green environmentNew ASG with ALB using cloud formation template

2) Adjust ASG size with production ASG

3) Switch DNS endpoint  from Blue to Green.



Architecture:

![New](https://github.com/deepak7093/DevOps/raw/master/cloudformation/LAMP-Blue-Green.png)
