odoo.define('edit_signup.is_mature', function(require) {
"use strict";

var publicWidget = require('web.public.widget');

publicWidget.registry.SignUpForm = publicWidget.Widget.extend({
    selector: '#date_of_birth',
    events: {
        'change': function() {
    date_of_birth = document.getElementById("date_of_birth").value
    if (date_of_birth != null && date_of_birth !='')
    {
    var dob = new Date(date_of_birth);
    var month_diff = Date.now() - dob.getTime();
    var age_dt = new Date(month_diff);
    var year = age_dt.getUTCFullYear();
    var age = Math.abs(year - 1970);
    if(age >= 18)
    {
    console.log(age)
    document.getElementById("is_mature").checked=true
    }else
    {
    document.getElementById("is_mature").checked=false
    console.log(age)

    }

    }

}
}
})
    })