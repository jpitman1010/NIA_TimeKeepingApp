$(document).ready(function(){
    $('input.timepicker-hours').timepicker({ 
        change: function(time) {
            // the input field
            let element = $(this), text;
            // get access to this Timepicker instance
            let timepicker = element.timepicker();
            text = 'Selected time is: ' + timepicker.format(time);
            element.siblings('span.help-line').text(text);
        },
        timeFormat: 'HH',
        interval: 1, // 1 minutes
        dropdown: true,
        scrollbar: true,
        dynamic: true,

    });
});


$(document).ready(function(){
    $('input.timepicker-first-min').timepicker({ 
        change: function(time) {
            // the input field
            let element = $(this), text;
            // get access to this Timepicker instance
            let timepicker = element.timepicker();
            text = 'Selected time is: ' + timepicker.format(time);
            element.siblings('span.help-line').text(text);
        },
        timeFormat: 'm',
        maxMinutes: 5,
        interval: 1, // 1 minutes
        dropdown: true,
        scrollbar: true,

    });
});

$(document).ready(function(){
    $('input.timepicker-second-min').timepicker({ 
        // change: function(time) {
        //     // the input field
        //     let element3 = $(this), text;
        //     // get access to this Timepicker instance
        //     let timepicker3 = element3.timepicker();
        //     text = timepicker3.format(time);
        //     element3.siblings('span.help-line').text(text);
        // },
        timeFormat: 'mm',
        maxMinutes: 9,
        interval: 1, // 1 minutes
        dropdown: true,
        scrollbar: true,

    });
});