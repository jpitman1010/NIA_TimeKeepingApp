(function($) {

	"use strict";

	// Setup the calendar with the current date
$(document).ready(function(){
    let date = new Date();
    let today = date.getDate();
    // Set click handlers for DOM elements
    $(".right-button").click({date: date}, next_year);
    $(".left-button").click({date: date}, prev_year);
    $(".month").click({date: date}, month_click);
    $("#add-button").click({date: date}, new_event);
    $("#change-button").click({date: date}, new_event);
    $("#day-calendar-button").click({date: date}, new_event);

    // Set current month as active
    $(".months-row").children().eq(date.getMonth()).addClass("active-month");
    init_calendar(date);
    let events = check_events(today, date.getMonth()+1, date.getFullYear());
    show_events(events, months[date.getMonth()], today, date.year);
});

// Initialize the calendar by appending the HTML dates
function init_calendar(date) {
    $(".tbody").empty();
    $(".events-container").empty();
    let calendar_days = $(".tbody");
    let month = date.getMonth();
    let year = date.getFullYear();
    let day_count = days_in_month(month, year);
    let row = $("<tr class='table-row'></tr>");
    let today = date.getDate();
    // Set date to 1 to find the first day of the month
    date.setDate(1);
    let first_day = date.getDay();
    // 35+firstDay is the number of date elements to be added to the dates table
    // 35 is from (7 days in a week) * (up to 5 rows of dates in a month)
    for(let i=0; i<35+first_day; i++) {
        // Since some of the elements will be blank, 
        // need to calculate actual date from index
        let day = i-first_day+1;
        // If it is a sunday, make a new row
        if(i%7===0) {
            calendar_days.append(row);
            row = $("<tr class='table-row'></tr>");
        }
        // if current index isn't a day in this month, make it blank
        if(i < first_day || day > day_count) {
            let curr_date = $("<td class='table-date nil'>"+"</td>");
            row.append(curr_date);
        }   
        else {
            let curr_date = $("<td class='table-date'>"+day+"</td>");
            let events = check_events(day, month+1, year);
            if(today===day && $(".active-date").length===0) {
                curr_date.addClass("active-date");
                show_events(events, months[month], day, year[year]);
            }
            // If this date has any events, style it with .event-date
            if(events.length!==0) {
                curr_date.addClass("event-date");
            }
            // Set onClick handler for clicking a date
            curr_date.click({events: events, month: months[month], day:day}, date_click);
            row.append(curr_date);
        }
    }
    // Append the last row and set the current year
    calendar_days.append(row);
    $(".year").text(year);
}

// Get the number of days in a given month/year
function days_in_month(month, year) {
    let monthStart = new Date(year, month, 1);
    let monthEnd = new Date(year, month + 1, 1);
    return (monthEnd - monthStart) / (1000 * 60 * 60 * 24);    
}

// Event handler for when a date is clicked
function date_click(event) {
    $(".events-container").show(250);
    $("#dialog").hide(250);
    $(".active-date").removeClass("active-date");
    $(this).addClass("active-date");
    console.log(this);
    show_events(event.data.events, event.data.month, event.data.day, event.data.year);
};

// Event handler for when a month is clicked
function month_click(event) {
    $(".events-container").show(250);
    $("#dialog").hide(250);
    let date = event.data.date;
    $(".active-month").removeClass("active-month");
    $(this).addClass("active-month");
    let new_month = $(".month").index(this);
    date.setMonth(new_month);
    init_calendar(date);
}

// Event handler for when the year right-button is clicked
function next_year(event) {
    $("#dialog").hide(250);
    let date = event.data.date;
    let new_year = date.getFullYear()+1;
    $("year").html(new_year);
    date.setFullYear(new_year);
    init_calendar(date);
}

// Event handler for when the year left-button is clicked
function prev_year(event) {
    $("#dialog").hide(250);
    let date = event.data.date;
    let new_year = date.getFullYear()-1;
    $("year").html(new_year);
    date.setFullYear(new_year);
    init_calendar(date);
}

$("#dialog").hide(250);
$(".events-container").show(250);

// Event handler for clicking the new event button
function new_event(event, year) {
    // if a date isn't selected then do nothing
    if($(".active-date").length===0)
        return;
    // remove red error input on click
    $("input").click(function(){
        $(this).removeClass("error-input");
    })
    // empty inputs and hide events
    $("#dialog input[type=text]").val('');
    $("#dialog input[type=number]").val('');
    $(".events-container").hide(250);
    $("#dialog").show(250);

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
    

    $('input.timepicker-first-min').timepicker({ 
        change: function(time) {
            // the input field
            let element = $(this), text;
            // get access to this Timepicker instance
            let timepicker = element.timepicker();
            text = timepicker.format(time);
            element.siblings('span.help-line').text(text);
        },
        timeFormat: 'm',
        maxMinutes: 5,
        interval: 1, // 1 minutes
        dropdown: true,
        scrollbar: true,

    });

    $('input.timepicker-second-min').timepicker({ 
        change: function(time) {
            // the input field
            let element3 = $(this), text;
            // get access to this Timepicker instance
            let timepicker3 = element3.timepicker();
            text = timepicker3.format(time);
            element3.siblings('span.help-line').text(text);
        },
        timeFormat: 'm',
        maxMinutes: 9,
        interval: 1, // 1 minutes
        dropdown: true,
        scrollbar: true,
    });
    // Event handler for cancel button
    $("#cancel-button").click(function() {
        $("#comment").removeClass("error-input");
        $("#time_entry").removeClass("error-input");
        $("#dialog").hide(250);
        $(".events-container").show(250);
    });
    // Event handler for ok button
    $("#ok-button").unbind().click({date: event.data.date}, function() {
        let date = event.data.date;
        let comment = $("#comment").val();
        let hour_entry = $('input.timepicker-hours');
        let first_min_entry = $('input.timepicker-first-minute');
        let second_min_entry = $('input.timepicker-second-minute');
        let time_entry = {hour_entry} + ':' + {first_min_entry} + {second_min_entry}
        let day = parseInt($(".active-date").html());

        // Form Handling to backend
        let formdata = new FormData(this);
        formdata.append('comment', comment);
        formdata.append('time_entry', time_entry);
        formdata.append('date', date);
        formdata.append('month', month);
        formdata.append('year', year);
        console.log(formdata)

        $.ajax({
            type: "POST",
            data: formdata,
            processData: false,
            contentType: false,
        }).done();

        // Basic form validation
        if(comment.length === 0) {
            $("#comment").addClass("error-input");
        }
        if(isNaN(time_entry)) {
            $("#timepicker-hour").addClass("error-input");
            $("#timepicker-first-min").addClass("error-input");
            $("#timepicker-second-min").addClass("error-input");

        }
        else {
            $("#dialog").hide(250);
            console.log("new event", (comment,time_entry, date, day));
            new_event_json(comment, time_entry, date, day);
            date.setDate(day);
            init_calendar(date);
        };
    });
}



// Adds a json event to event_data
function new_event_json(comment, time_entry, date, day) {
    let event = {
        "comment": comment,
        "time_entry": time_entry,
        "year": date.getFullYear(),
        "month": date.getMonth()+1,
        "day": day
    };
    event_data["events"].push(event);
}

// Display all events of the selected date in card views
function show_events(events, month, day, year) {
    // Clear the dates container
    $(".events-container").empty();
    $(".events-container").show(250);
    console.log(event_data["events"]);
    // If there are no events for this date, notify the user
    if(events.length===0) {
        let event_card = $("<div class='event-card'></div>");
        let event_name = $("<div class='event-name'>There are no events planned for "+month+" "+day+".</div>");
        $(event_card).css({ "border-left": "10px solid #FF1744" });
        $(event_card).append(event_name);
        $(".events-container").append(event_card);

        let formdata = new FormData(this);
        formdata.append('month', month);
        formdata.append('date', day);
        formdata.append('year', year);

        $.ajax({
            type: "POST",
            data: formdata,
            processData: false,
            contentType: false,
        }).done();

    }
    else {
        // Go through and add each event as a card to the events container
        for(let i=0; i<events.length; i++) {
            let event_card = $("<div class='event-card'></div>");
            let event_name = $("<div class='event-name'>"+events[i]["comment"]+"</div>");
            let event_count = $("<div class='event-count'>"+events[i]["time_entry"]+"</div>");
            if(events[i]["cancelled"]===true) {
                $(event_card).css({
                    "border-left": "10px solid #FF1744"
                });
                event_count = $("<div class='event-cancelled'>Cancelled</div>");
            }
            $(event_card).append(event_name).append(event_count);
            $(".events-container").append(event_card);
        }
    }
}

// Checks if a specific date has any events
function check_events(day, month, year) {
    let events = [];
    for(let i=0; i<event_data["events"].length; i++) {
        let event = event_data["events"][i];
        if(event["day"]===day &&
            event["month"]===month &&
            event["year"]===year) {
                events.push(event);
            }
    }
    return events;
}

// Given data for events in JSON format
let event_data = {
    "events": [
    {
        "comment": " Repeated Test Event ",
        "time_entry": 120,
        "year": 2020,
        "month": 5,
        "day": 10,
        "cancelled": true
    },
    {
        "comment": " Repeated Test Event ",
        "time_entry": 120,
        "year": 2020,
        "month": 5,
        "day": 10,
        "cancelled": true
    },
        {
        "comment": " Repeated Test Event ",
        "time_entry": 120,
        "year": 2020,
        "month": 5,
        "day": 10,
        "cancelled": true
    },
    {
        "comment": " Repeated Test Event ",
        "time_entry": 120,
        "year": 2020,
        "month": 5,
        "day": 10
    },
        {
        "comment": " Repeated Test Event ",
        "time_entry": 120,
        "year": 2020,
        "month": 5,
        "day": 10,
        "cancelled": true
    },
    {
        "comment": " Repeated Test Event ",
        "time_entry": 120,
        "year": 2020,
        "month": 5,
        "day": 10
    },
        {
        "comment": " Repeated Test Event ",
        "time_entry": 120,
        "year": 2020,
        "month": 5,
        "day": 10,
        "cancelled": true
    },
    {
        "comment": " Repeated Test Event ",
        "time_entry": 120,
        "year": 2020,
        "month": 5,
        "day": 10
    },
        {
        "comment": " Repeated Test Event ",
        "time_entry": 120,
        "year": 2020,
        "month": 5,
        "day": 10,
        "cancelled": true
    },
    {
        "comment": " Repeated Test Event ",
        "time_entry": 120,
        "year": 2020,
        "month": 5,
        "day": 10
    },
    {
        "comment": " Test Event",
        "time_entry": 120,
        "year": 2020,
        "month": 5,
        "day": 11
    }
    ]
};

const months = [ 
    "January", 
    "February", 
    "March", 
    "April", 
    "May", 
    "June", 
    "July", 
    "August", 
    "September", 
    "October", 
    "November", 
    "December" 
];

})(jQuery);
