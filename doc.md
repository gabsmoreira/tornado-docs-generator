****
## **ChangePassword**

****
## **Client**

```/client```
### <div style="color:orange">Post</div>
#### Description:
Client creation route
#### Response:
##### <div style="color:green">Code: 200</div>
!!! success
      ```{"name": "string", "age": "int"}```
 
 
##### <div style="color:red">Code: 401</div>
!!! failure 
      ```{"message": "hehehehe"}```
 
 
#### Parameters:
##### Header parameters:
| key | value | 
 |-|-| 
| Authorization | token | 
| Content-Type | application/json | 

##### Path parameters:
| Name | Description | 
 |-|-| 
| id | client id from db | 

### <div style="color:green">Get</div>
#### Description:
Client creation route
#### Parameters:
##### Header parameters:
| key | value | 
 |-|-| 
| Authorization | token | 
| Content-Type | application/json | 

##### Path parameters:
| Name | Description | 
 |-|-| 
| id | client id from db | 

##### Body parameters:
```json
{"name": {"type": "string"}, "phone": {"type": "string"}, "email": {"type": "string"}, "password": {"type": "string"}}
```
#### Response:
##### <div style="color:green">Code: 200</div>
!!! success
      ```{"name": "string", "age": "int"}```
 
 
##### <div style="color:red">Code: 401</div>
!!! failure 
      ```{"message": "hehehehe"}```
 
 
