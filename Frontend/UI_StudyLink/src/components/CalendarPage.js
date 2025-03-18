import React, { useState, useEffect } from 'react';
import { Calendar, dateFnsLocalizer } from 'react-big-calendar';
import format from 'date-fns/format';
import parse from 'date-fns/parse';
import startOfWeek from 'date-fns/startOfWeek';
import getDay from 'date-fns/getDay';
import addDays from 'date-fns/addDays';
import addWeeks from 'date-fns/addWeeks';
import addMonths from 'date-fns/addMonths';
import isBefore from 'date-fns/isBefore';
import isEqual from 'date-fns/isEqual';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import './CalendarPage.css';
import { useSelector } from 'react-redux';
import { hsl } from 'color-convert';
import { setGroups } from '../redux/features/groupSlice';
import { useDispatch } from 'react-redux';

const locales = {
  'en-US': require('date-fns/locale/en-US'),
};

const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales,
});


const CalendarPage = () => {
  const [events, setEvents] = useState([]);
  const [fetchedGroups, setFetchedGroups] = useState([]);
  const loggedUser = useSelector(state => state.login.loggedUser) || JSON.parse(localStorage.getItem('user'));
  const apiBaseGroups = process.env.REACT_APP_API_GROUPS;
  const dispatch = useDispatch();

  useEffect(() => {
    const fetchGroups = async () => {
      try {
        const response = await fetch(`${apiBaseGroups}/study-group`, {
          headers: {
            'token': loggedUser.canvas_token
          }
        });
        
        if (!response.ok) {
          const errorData = await response.text();
          console.error('API Error:', response.status, errorData);
          throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();

        setFetchedGroups(data.data || []);
        dispatch(setGroups(data.data || []));
      } catch (error) {
        console.error('Error fetching groups:', error);
        setFetchedGroups([]);
      }
    };

    fetchGroups();
  }, [apiBaseGroups, loggedUser.canvas_token, dispatch]);


  useEffect(() => {
    const userEvents = fetchedGroups
      .filter(group => group.members.includes(loggedUser.user_id))
      .flatMap(group => {
        const startDate = new Date(`${group.meeting_date}T${group.start_time}`);
        const endDate = new Date(`${group.meeting_date}T${group.end_time}`);
        const baseEvent = {
          id: group.group_id,
          title: group.group_name,
          start: startDate,
          end: endDate,
          createdBy: group.created_by,
          recurring: group.is_recurring,
          recurrenceFrequency: group.recurrence_frequency,
          recurrenceEndDate: group.recurrence_end_date ? new Date(group.recurrence_end_date + 'T23:59:59'): null,
        };
        if (group.is_recurring && group.recurrence_end_date) {
          const recurringEvents = generateRecurringEvents(baseEvent);
          return recurringEvents;
        } else {
          return [baseEvent];
        }
      });
    setEvents(userEvents);
  }, [fetchedGroups]);

  const generateRecurringEvents = (baseEvent) => {
    const events = [];
    let currentDate = new Date(baseEvent.start);
    const endDate = baseEvent.recurrenceEndDate ? new Date(baseEvent.recurrenceEndDate) : null;
    const maxRecurringEvents = 365;
    
    while ((!endDate || isBefore(currentDate, endDate)) && events.length < maxRecurringEvents) {
      const eventDuration = baseEvent.end.getTime() - baseEvent.start.getTime();
      events.push({
        ...baseEvent,
        id: `${baseEvent.id}-${currentDate.getTime()}`,
        start: new Date(currentDate),
        end: new Date(currentDate.getTime() + eventDuration)
      });

      if (baseEvent.recurrenceFrequency.toLowerCase() === 'daily') {
        currentDate = addDays(currentDate, 1);
      } else if (baseEvent.recurrenceFrequency.toLowerCase() === 'weekly') {
        currentDate = addWeeks(currentDate, 1);
      } else if (baseEvent.recurrenceFrequency.toLowerCase() === 'monthly') {
        currentDate = addMonths(currentDate, 1);
      } else {
        break; 
      }
    }

    return events;
  };


  const generateEventColor = (eventId) => {
    const baseId = typeof eventId === 'string' ? eventId.split('-')[0] : eventId.toString();
    
    let hash = 0;
    for (let i = 0; i < baseId.length; i++) {
      hash = baseId.charCodeAt(i) + ((hash << 5) - hash);
    }
    const hue = hash % 360;
    const [r, g, b] = hsl.rgb([hue, 70, 80]);
    return `rgb(${r}, ${g}, ${b})`;
  };

  const eventStyleGetter = (event, start, end, isSelected) => {
    const backgroundColor = generateEventColor(event.id);
    let style = {
      backgroundColor,
      borderRadius: '0px',
      opacity: 0.8,
      color: 'black',
      border: '0px',
      display: 'block'
    };

    if (isSelected) {
      style.backgroundColor = 'orange';
    }

    return {
      style: style
    };
  };

  const EventComponent = ({ event }) => (
    <div className="rbc-event-content">
      <strong>{event.title}</strong>
    </div>
  );

  return (
    <div className="calendar-page">
      <h1>Calendar</h1>
      <Calendar
        localizer={localizer}
        events={events}
        startAccessor="start"
        endAccessor="end"
        style={{ height: 500 }}
        eventPropGetter={eventStyleGetter}
        components={{
          event: EventComponent
        }}
      />
    </div>
  );
};

export default CalendarPage;
