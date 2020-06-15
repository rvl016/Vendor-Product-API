<h1> Vendor-Product - JSON API </h1>

___

<h2>All API Endpoints</h2>
<br/>

<b>GET</b> on `/api/vendors`<br/>

<b>POST</b> on `/api/vendors`<br/>

<b>DELETE</b> on `/api/vendors`<br/>

___

<b>GET</b> on `/api/vendors/<vendor_id>`<br/>

<b>PUT</b> on `/api/vendors/<vendor_id>`<br/>

<b>DELETE</b> on `/api/vendors/<vendor_id>`<br/>

___

<b>GET</b> on `/api/vendors/<vendor_id>/products`<br/>

<b>POST</b> on `/api/vendors/<vendor_id>/products`<br/>

___

<b>GET</b> on `/api/products`<br/>

<b>DELETE</b> on `/api/products`<br/>

___

<b>GET</b> on `/api/prducts/<product_id>`<br/>

<b>PUT</b> on `/api/prducts/<product_id>`<br/>

<b>DELETE</b> on `/api/prducts/<product_id>`<br/>


<h2>How to view, register and delete vendors</h2>
<br/>

This is done on `/api/vendors` endpoint:</br>

<h4>Viewing all vendors:</h4>
<br/>
Send a <b>GET</b> on `/api/vendors`. Your response will contain the following:

<br/><br/>

```js
"data": [
  {
    "id": 0,
    "name": "'Vendor 0 Name'",
    "cnpj": "'Vendor 0 CNPJ'",
    "city": "'Vendor 0 city'"
  },
  {
    "id": 1,
    "name": "'Vendor 1 Name'",
    "cnpj": "'Vendor 1 CNPJ'",
    "city": "'Vendor 1 city'"
  }
]
```

> If there are no vendors on the database, your response status will be a 204, instead of 200.

<br/>

<h4>Registering a new vendor:</h4>
<br/>
Send a <b>POST</b> on `/api/vendors`. Your request body must be like the following:

<br/><br/>

```js
"vendor": {
  "name": "'Vendor Name'",
  "cnpj": "XX.XXX.XXX/XXXX-XX",   // Make sure CNPJ is in full standard format
  "city": "'Vendor city'"
}
```

> If validation fails, you will receive a 406 status with 'errors' key in the body. Also, make sure the CNPJ does not exist in the database.

<br/>

<h4>Deleting vendors:</h4>
<br/>
Send a <b>DELETE</b> on `/api/vendors`. Your request body must be like the following:

<br/><br/>

```js
"vendors": [
  0,    // Vendor id, as you can see in the GET request
  1
]
```

> The validation on this request only requires that 'vendors' is an array of integers. If some id does not exist, it will be ignored and the existent ones will be deleted and the response status will be a 200 anyway.

> Warning: All vendor's products data will be lost.

<h2>How to view, modify and delete a specific vendor</h2>
<br/>

This is done on `/api/vendors/<vendor_id>` endpoint:</br>

<h4>Viewing a vendor:</h4>
<br/>
Send a <b>GET</b> on `/api/vendors`. Your response will contain the following:

<br/><br/>

```js
"data": {
   "id": 0,
   "name": "'Vendor 0 Name'",
   "cnpj": "'Vendor 0 CNPJ'",
   "city": "'Vendor 0 city'"
}
```

> If the requested 'vendor_id' does no exist, your response will be a 404.

<h4>Modifying a vendor data:</h4>
<br/>
Send a <b>PUT</b> on `/api/vendors/<vendor_id>`. Your request body must contain the following:

<br/><br/>

```js
"vendor": {
   "name": "'Vendor 0 Name'",
   "cnpj": "'Vendor 0 CNPJ'",
   "city": "'Vendor 0 city'"
}
```

> You don't have to specify all the fields, only those you want to modify.

> If the requested 'vendor_id' does no exist, your response will be a 404.

<h4>Deleting a vendor:</h4>
<br/>
Send a <b>DELETE</b> on `/api/vendors/<vendor_id>`.
<br/>

> If the requested 'vendor_id' does no exist, your response will be a 404.

> Warning: All vendor's products data will be lost.


<h2>How to view, create and delete products</h2>
</br>

<h4>Viewing all products of any vendor:</h4>
<br/>
Send a <b>GET</b> on `/api/products`. Your response will contain the following:

<br/><br/>

```js
"data": [
  {
    "id": 0,
    "vendor_id": 1,
    "vendor_name": "'Vendor 1 Name'",
    "name": "'Product 0 Name'",
    "code": "'Product 0 Code'",
    "price": "'Product 0 Price'"
  },
  {
    "id": 1,
    "vendor_id": 1,
    "vendor_name": "'Vendor 1 Name'",
    "name": "'Product 1 Name'",
    "code": "'Product 1 Code'",
    "price": "'Product 1 Price'"
  },
  {
    "id": 2,
    "vendor_id": 2,
    "vendor_name": "'Vendor 2 Name'",
    "name": "'Product 2 Name'",
    "code": "'Product 2 Code'",
    "price": "'Product 2 Price'"
  }
]
```
<br/>

> If there are no products on the database, your response status will be a 204, instead of 200.

<h4>Viewing all products of a specific vendor:</h4>
<br/>
Send a <b>GET</b> on `/api/vendors/<vendor_id>/products`. Your response will contain the following:

<br/><br/>

```js
"data": [
  {
    "id": 0,
    "name": "'Product 0 Name'",
    "code": "'Product 0 Code'",
    "price": "'Product 0 Price'"
  },
  {
    "id": 1,
    "name": "'Product 1 Name'",
    "code": "'Product 1 Code'",
    "price": "'Product 1 Price'"
  }
]
```
<br/>

> If there are no products for the vendor on the database, your response status will be a 204, instead of 200.

<h4>Creating a new product for a specific vendor:</h4>
<br/>
Send a <b>POST</b> on `/api/vendors/<vendor_id>/products`. Your request body must be like the following:

<br/><br/>

```js
"product": {
   "name": "'Product 0 Name'",
   "code": "XXXXXXXXXXXX",     // A string of numbers with UPC-A format.
   "price": "'Product 0 Price'"
}
```

> The product code must be unique for each vendor.

> If the requested 'vendor_id' does no exist, your response will be a 404.

<h4>Deleting products:</h4>
<br/>
Send a <b>DELETE</b> on `/api/vendors/products`. Your request body must be like the following:

<br/><br/>

```js
"products": [
   1,
   2,
   3   
]
```

> The validation on this request only requires that 'products' is an array of integers. If some id does not exist, it will be ignored and the existent ones will be deleted and the response status will be a 200 anyway.

> The ids on the array are same you see on the two get requests showed previously.


<h2>How to view, create and delete a specific product</h2>
</br>

<h4>Viewing a specific product:</h4>
<br/>
Send a <b>GET</b> on `/api/products/<product_id>`. Your response body will be like the following:

```js
"data": {
   "id": 0,
   "vendor_id": 1,
   "vendor_name": "'Vendor 1 Name'",
   "name": "'Product 0 Name'",
   "code": "'Product 0 Code'",
   "price": "'Product 0 Price'"
} 
```

> If the requested 'product_id' does no exist, your response will be a 404.

<h4>Modifying a specific product:</h4>
<br/>
Send a <b>PUT</b> on `/api/products/<product_id>`. Your request body should be like the following:

```js
"product": {
   "name": "'Product 0 Name'",
   "code": "XXXXXXXXXXXX",     // A string of numbers with UPC-A format.
   "price": "'Product 0 Price'"
} 
```

> You don't have to specify all the fields (only those in above can be modified), only those you want to modify. 

> If the requested 'product_id' does no exist, your response will be a 404.

<h4>Deleting a specific product:</h4>
<br/>
Send a <b>DELETE</b> on `/api/products/<product_id>`.
<br/>

> If the requested 'vendor_id' does no exist, your response will be a 404.
