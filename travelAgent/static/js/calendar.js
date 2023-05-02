let reservation = [];
let destinations = [];
let attractions = [];
let accommodations = [];
let traffics = [];

$.ajax({
    url: "data",
    type: "POST",
    dataType: "json",
    success: function (data) {
        // var data = JSON.parse(data)
        var dates = data[0].date;
        var destination = data[1].destination;
        var attraction = data[2].attraction;
        var accommodation = data[3].accommodation;
        var traffic = data[4].traffic;

        //time
        for (let i = 0; i < dates.length; i++) {
            let ary = dates[i].split('-')
            console.log(ary)
            dates[i] = new Date(ary[0], ary[1] - 1, ary[2])
            reservation.push(dates[i])
            // console.log(dates[i])
        }
    //    detail
        for (let i = 0; i < destination.length; i++) {
            destinations.push(destination[i])
            console.log(destination[i])
        }
        for (let i = 0; i < attraction.length; i++) {
            attractions.push(attraction[i])
            console.log(attraction[i])
        }
        for (let i = 0; i < accommodation.length; i++) {
            accommodations.push(accommodation[i])
            console.log(accommodation[i])
        }
        for (let i = 0; i < traffic.length; i++) {
            traffics.push(traffic[i])
            console.log(traffic[i])
        }

        let d = new Date()
        month = d.getMonth()
        year = d.getFullYear()
        generateCalendar(month,year)

    }
});

//找出lst中所有索引的位置
function indexAll(arr, ele){
    var indexlist = []
    for( var i = 0; i < arr.length; i++){
        console.log("1" + typeof arr[i])
        if(arr[i].getTime() === ele.getTime()){
            indexlist.push(i);
        }
    }
    return indexlist;
}

function checkDetail(d){
    index_lst = indexAll(reservation, d)
    if (index_lst.length > 0 ){
        for(let i = 0; i < index_lst.length; i++){
            index = index_lst[i]
            destinaion = destinations[index] //已经是名字了
            attraction = attractions[index]  //剩下的全是dictionary
            accommodation = accommodations[index]
            traffic = traffics[index]

            var html = '<div class="detail_date"  style="font-size: larger">\n' +
            '            Destination: <kbd class="destination_date">' + destinaion + ' </kbd> <br/>\n' +
            '            Attraction: <kbd class="attraction_date">'  + attraction.name + '</kbd> <br/>\n' +
            '                      Introduction: <code class="attraction_date">'  + attraction.intro + '</code> <br/>\n' +
            '            Accommodation: <kbd class="accommodation_date"> ' + accommodation.name + '</kbd> <br/>\n' +
            '                      Introduction: <code class="attraction_date">'  + accommodation.intro + '</code> <br/>\n' +
            '            Traffic: <kbd class="traffic_date">' + traffic.name + '</kbd> <br/>\n' +
            '                      Introduction: <code class="attraction_date">'  + traffic.intro + '</code> <br/>\n' +
            '        </div>'

            $("#calendar_container").html(html);
            // $("#calendar_container").append(html)
        }
    }
    $("#calendar_container").html();

}


// for (let i=0; i < days.length; i++){
//     console.log(days[i].getDate())
// }

const isLeapYear = (year) => {
    return (
        (year % 4 === 0 && year % 100 !== 0 && year % 400 !== 0) ||
        (year % 100 === 0 && year % 400 === 0)
    );
};
const getFebDays = (year) => {
    return isLeapYear(year) ? 29 : 28;
};
let calendar = document.querySelector('.calendar');
const month_names = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
];
let month_picker = document.querySelector('#month-picker');
const dayTextFormate = document.querySelector('.day-text-formate');
const timeFormate = document.querySelector('.time-formate');
const dateFormate = document.querySelector('.date-formate');

month_picker.onclick = () => {
    month_list.classList.remove('hideonce');
    month_list.classList.remove('hide');
    month_list.classList.add('show');
    dayTextFormate.classList.remove('showtime');
    dayTextFormate.classList.add('hidetime');
    timeFormate.classList.remove('showtime');
    timeFormate.classList.add('hideTime');
    dateFormate.classList.remove('showtime');
    dateFormate.classList.add('hideTime');
};

const generateCalendar = (month, year) => {
    let calendar_days = document.querySelector('.calendar-days');
    calendar_days.innerHTML = '';
    let calendar_header_year = document.querySelector('#year');
    let days_of_month = [
        31,
        getFebDays(year),
        31,
        30,
        31,
        30,
        31,
        31,
        30,
        31,
        30,
        31,
    ];

    let currentDate = new Date();

    month_picker.innerHTML = month_names[month];

    calendar_header_year.innerHTML = year;

    let first_day = new Date(year, month);


    for (let i = 0; i <= days_of_month[month] + first_day.getDay() - 1; i++) {


        let day = document.createElement('div');

        if (i >= first_day.getDay()) {
            day.innerHTML = i - first_day.getDay() + 1;

            if (i - first_day.getDay() + 1 === currentDate.getDate() && year === currentDate.getFullYear() &&
                month === currentDate.getMonth() ) {
                console.log(currentDate);
                day.classList.add('current-date');


                // console.log(reservation)
                //
                // for (let j = 0; j < reservation.length; j++) {
                //     if (day.innerHTML === reservation[j].date) {
                //         day.classList.add('reservation');
                //     }
                // }
            }
            for (let j = 0; j < reservation.length; j++) {
                console.log(reservation[j])
                // if (i - first_day.getDay() + 1 === currentDate.getDate() && year === currentDate.getFullYear() &&
                //     month === currentDate.getMonth()) {
                    if (i - first_day.getDay() + 1 === reservation[j].getDate() && year === reservation[j].getFullYear() &&
                        month === reservation[j].getMonth()) {
                    // if (i - first_day.getDay() + 1 === r_day && year === r_year &&
                    //     month === r_month) {
                        day.classList.add('reservation');
                    }
                }

            }
            calendar_days.appendChild(day);
            day.onclick = (el) => {
                let days = el.currentTarget.innerText
                // console.log(days)
                clicked_month = month + 1
                // clicked_year = year


                let date_new = year + "-" + clicked_month + "-" + days
                // console.log(date_new)
                let d = date_new.split('-')
                dates_new = new Date(d[0], d[1] - 1, d[2])
                console.log("dates_new type = " +  typeof dates_new)
                checkDetail(dates_new)
            }
        }


    }
    ;
//end generateCalendar



    let month_list = calendar.querySelector('.month-list');
    month_names.forEach((e, index) => {
        let month = document.createElement('div');
        month.innerHTML = `<div>${e}</div>`;

        month_list.append(month);
        month.onclick = () => {
            currentMonth.value = index;
            generateCalendar(currentMonth.value, currentYear.value);
            month_list.classList.replace('show', 'hide');
            dayTextFormate.classList.remove('hideTime');
            dayTextFormate.classList.add('showtime');
            timeFormate.classList.remove('hideTime');
            timeFormate.classList.add('showtime');
            dateFormate.classList.remove('hideTime');
            dateFormate.classList.add('showtime');
        };
    });

    (function () {
        month_list.classList.add('hideonce');
    })();
    document.querySelector('#pre-year').onclick = () => {
        --currentYear.value;
        generateCalendar(currentMonth.value, currentYear.value);
    };
    document.querySelector('#next-year').onclick = () => {
        ++currentYear.value;
        generateCalendar(currentMonth.value, currentYear.value);
    };

    let currentDate = new Date();
    let currentMonth = {value: currentDate.getMonth()};
    let currentYear = {value: currentDate.getFullYear()};
    generateCalendar(currentMonth.value, currentYear.value);

    const todayShowTime = document.querySelector('.time-formate');
    const todayShowDate = document.querySelector('.date-formate');

    const currshowDate = new Date();
    const showCurrentDateOption = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long',
    };
    const currentDateFormate = new Intl.DateTimeFormat(
        'en-US',
        showCurrentDateOption
    ).format(currshowDate);
    todayShowDate.textContent = currentDateFormate;
    setInterval(() => {
        const timer = new Date();
        const option = {
            hour: 'numeric',
            minute: 'numeric',
            second: 'numeric',
        };
        const formateTimer = new Intl.DateTimeFormat('en-us', option).format(timer);
        let time = `${`${timer.getHours()}`.padStart(
            2,
            '0'
        )}:${`${timer.getMinutes()}`.padStart(
            2,
            '0'
        )}: ${`${timer.getSeconds()}`.padStart(2, '0')}`;
        todayShowTime.textContent = formateTimer;
    }, 1000);






