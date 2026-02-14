משה אלמליח 322534348 כיתת נגב

# run `docker compose up -d`

## to see in mysql 
* run `docker exec -it mysql mysql -u user -ppassword`

## to see mongodb in compase
* create connection in uri `mongodb://mongo:27017`

## commends curl in cmd 
### route 1
run `curl -X GET http://localhost:8000/analytics/top-customers`
### route 2
run `curl -X GET http://localhost:8000/analytics/customers-without-orders`
### route 3
run `curl -X GET http://localhost:8000/analytics/zero-credit-active-customers`
