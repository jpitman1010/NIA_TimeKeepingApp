(function ($) {

    "use strict";

    // Setup the calendar with the current date
    $(document).ready(function () {
    
        let date = new Date();
        let today = date.getDate()
        $(today).addClass('today');
        // Set click handlers for DOM elements
        $(".right-button").click({
            date: date
        }, next_year);
        $(".left-button").click({
            date: date
        }, prev_year);
        $(".month").click({
            date: date
        }, month_click);
        
        // Set current month as active
        $(".months-row").children().eq(date.getMonth()).addClass("active-month");
        init_calendar(date);
        
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
        for (let i = 0; i < 35 + first_day; i++) {
            // Since some of the elements will be blank, 
            // need to calculate actual date from index
            let day = i - first_day + 1;
            // If it is a sunday, make a new row
            if (i % 7 === 0) {
                calendar_days.append(row);
                row = $("<tr class='table-row'></tr>");
            }
            // if current index isn't a day in this month, make it blank
            if (i < first_day || day > day_count) {
                let curr_date = $("<td class='table-date nil'>" + "</td>");
                row.append(curr_date);
            } else {
                let curr_date = $("<td class='table-date'>" + day + "</td>");
               

                // Set onClick handler for clicking a date
                curr_date.click({
                    month: months[month],
                    day: day
                }, date_click);
                row.append(curr_date);
                console.log(curr_date.month, curr_date.day,curr_date.year)
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
    function date_click() {
        $(".events-container").show(250);
        $("#dialog").hide(250);
        $(".active-date").removeClass("active-date");
        $(this).addClass("active-date");
        console.log('date_click fcn in script.js this===', this)

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
        let new_year = date.getFullYear() + 1;
        $("year").html(new_year);
        date.setFullYear(new_year);
        init_calendar(date);
    }

    // Event handler for when the year left-button is clicked
    function prev_year(event) {
        $("#dialog").hide(250);
        let date = event.data.date;
        let new_year = date.getFullYear() - 1;
        $("year").html(new_year);
        date.setFullYear(new_year);
        init_calendar(date);
    }

    $("#dialog").hide(250);
    $(".events-container").show(250);

    function show_events(month, day) {
        $(".events-container").empty();
        $(".events-container").show(250);
        let event_card = $("<div class='event-card'></div>");
        let event_name = $("<div class='event-name'>There are no events planned for "+month+" "+day+".</div>");
        $(event_card).css({ "border-left": "10px solid #FF1744" });
        $(event_card).append(event_name);
        $(".events-container").append(event_card);
    }

   
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