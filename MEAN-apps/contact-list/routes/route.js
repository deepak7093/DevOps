const express = require('express');
var router = express.Router();
var Contact = require('../model/contact');

router.get('/contact', function(req, res, callback){
    Contact.find(function(err, contact){
        res.json(contact);
    })
});


router.post('/contact', function(req, res, next){
    let newContact = new Contact({
        first_name: req.body.first_name,
        last_name: req.body.last_name,
        phone: req.body.phone

    });
    newContact.save(function(err, contact){
        if(err){
            res.json({msg: 'Failed to add Contact'});
        }
        else{
            res.json({msg: 'Successful added contact'});
        }
    })
});

router.post('/addContact', function(req, res){
    let newContact = new Contact({
        first_name: req.body.first_name,
        last_name: req.body.last_name,
        phone: req.body.phone

    });
    newContact.save(function(err, contact){
        if(err){
            res.json({msg: 'Failed to add Contact'});
        }
        else{
            res.json({msg: 'Successful added contact'});
        }
    })
})

module.exports = router;
