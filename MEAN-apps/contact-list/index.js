var express = require('express');
var bodyParser = require('body-parser');
var path = require('path');
var mongoose = require('mongoose');
var cors = require('cors');

var  app = express();

const routes = require('./routes/route');
// Connenct to mongodb
mongoose.connect('mongodb://localhost:27017/contactlist');
mongoose.connection.on('connected', function(){
    console.log('Connect successful to mongo');
})

mongoose.connection.on('error', function(err){
    console.err('Error to connect mongo');
})
app.use(bodyParser.json());
app.use(cors());
app.use(express.static(path.join(__dirname, 'public')));
app.use('/api', routes);


const port = 3000;

app.get('/', function(req, res) {
    res.send('Hello-World');
})

app.listen(port, function(req, res){
    console.log("Server listing on port:", +port);
})