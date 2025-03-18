import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux'; 
import { setGroups, addGroup, updateGroup, deleteGroup } from '../redux/features/groupSlice';
import { setCourses } from '../redux/features/courseSlice';
import './StudyGroups.css';

function StudyGroups() {
  const [groups, setFetchedGroups] = useState([]);
  const loggedUser = useSelector(state => state.login.loggedUser) || JSON.parse(localStorage.getItem('user'));
  const [courses, setUserCourses] = useState([]);
  const dispatch = useDispatch();
  const apiBaseCourses = process.env.REACT_APP_API_COURSES;
  const apiBaseGroups = process.env.REACT_APP_API_GROUPS;

  
  const [newGroup, setNewGroup] = useState({ 
    group_name: '', 
    created_by: '', 
    created_at: '',
    course_id: '',
    is_recurring: false, 
    meeting_date: '', 
    recurrence_frequency: '', 
    recurrence_end_date: '', 
    start_time: '',
    end_time: '',
    members: []
  });
  const [searchTerm, setSearchTerm] = useState('');
  const currentUser = loggedUser.user_id
  const navigate = useNavigate();
  const [isEditing, setIsEditing] = useState(false);
  const [dateError, setDateError] = useState('');

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await fetch(`${apiBaseCourses}/users/${loggedUser.user_id}/courses`, {
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
        dispatch(setCourses(data.courses));
        setUserCourses(data.courses);
      } catch (error) {
        console.error('Error fetching courses:', error);
        setUserCourses([]);
      }
    };
    fetchCourses();
  }, [apiBaseCourses, loggedUser.user_id, loggedUser.canvas_token, dispatch]);

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

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    const newValue = type === 'checkbox' ? checked : value;

    setNewGroup(prevGroup => {
      const updatedGroup = { ...prevGroup, [name]: newValue };

      // Validate recurrence end date
      if (name === 'recurrence_end_date' || name === 'meeting_date') {
        if (updatedGroup.recurrence_end_date && updatedGroup.meeting_date) {
          if (new Date(updatedGroup.recurrence_end_date) < new Date(updatedGroup.meeting_date)) {
            setDateError('Recurrence end date must be later than or equal to the start date');
          } else {
            setDateError('');
          }
        }
      }

      // Adjust end time if it's before start time
      if (name === 'start_time' && updatedGroup.end_time && value > updatedGroup.end_time) {
        updatedGroup.end_time = value;
      }

      return updatedGroup;
    });
  };

  const handleCreateGroup = async (e) => {
    e.preventDefault();
    if (dateError) {
      alert('Please correct the date error before submitting.');
      return;
    }
    if (newGroup.group_name && newGroup.course_id && newGroup.meeting_date && newGroup.start_time && newGroup.end_time) {
      if (isEditing) {
        console.log('updating group', newGroup)
        console.log(`${apiBaseGroups}/${loggedUser.user_id}/study-group/${newGroup.group_id}`)
        try {
          const response = await fetch(`${apiBaseGroups}/${loggedUser.user_id}/study-group/${newGroup.group_id}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${loggedUser.jwt_token}`,
              'Google-Token': `${loggedUser.credentials}`
            },
            body: JSON.stringify(newGroup)
          });

          if (!response.ok) {
            const errorData = await response.text();
            console.error('API Error:', response.status, errorData);
            throw new Error(`API error: ${response.status}`);
          }

          setFetchedGroups(prevGroups => prevGroups.map(group => 
            group.group_id === newGroup.group_id ? newGroup : group
          ));
          
          setIsEditing(false);
          setNewGroup({ 
            group_name: '', 
            created_by: '', 
            created_at: '',
            course_id: '',
            is_recurring: false, 
            meeting_date: '', 
            recurrence_frequency: '', 
            recurrence_end_date: '', 
            start_time: '',
            end_time: '',
            members: []
          });
          alert('Group updated successfully');
        } catch (error) {
          console.error('Error updating group:', error);
          alert('Failed to update group. Please try again.');
        }
      } else {
        try {
          const newGroupWithId = {
            ...newGroup,
            members: [loggedUser.user_id],
            created_by: loggedUser.user_id,
            created_at: new Date().toISOString() 
          };

          const response = await fetch(`${apiBaseGroups}/${loggedUser.user_id}/study-group`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${loggedUser.jwt_token}`,
              'Google-Token': `${loggedUser.credentials}`
            },
            body: JSON.stringify(newGroupWithId)
          });

          if (!response.ok) {
            const errorData = await response.text();
            console.error('API Error:', response.status, errorData);
            throw new Error(`API error: ${response.status}`);
          }

          const createdGroup = await response.json();
          
          setFetchedGroups(prevGroups => [newGroupWithId, ...prevGroups]);
          dispatch(addGroup(newGroupWithId));

          setNewGroup({ 
            group_name: '', 
            created_by: '', 
            created_at: '',
            course_id: '',
            is_recurring: false, 
            meeting_date: '', 
            recurrence_frequency: '', 
            recurrence_end_date: '', 
            start_time: '',
            end_time: '',
            members: []
          });
        } catch (error) {
          console.error('Error creating group:', error);
          alert('Failed to create group. Please try again.');
        }
      }
    } else {
      alert('Please fill in all fields');
    }
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleJoinGroup = async (group_id) => {
    try {
      const group = groups.find(g => g.group_id === group_id);
      const updatedMembers = {
        members: [...group.members, loggedUser.user_id]
      };

      const response = await fetch(`${apiBaseGroups}/${loggedUser.user_id}/study-group/${group_id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${loggedUser.jwt_token}`,
          'Google-Token': `${loggedUser.credentials}`
        },
        body: JSON.stringify(updatedMembers)
      });

      if (!response.ok) {
        const errorData = await response.text();
        console.error('API Error:', response.status, errorData);
        throw new Error(`API error: ${response.status}`);
      }

      setFetchedGroups(prevGroups => 
        prevGroups.map(group => {
          if (group.group_id === group_id && !group.members.includes(loggedUser.user_id)) {
            return { ...group, members: updatedMembers.members };
          }
          return group;
        })
      );

    } catch (error) {
      console.error('Error joining group:', error);
      alert('Failed to join group. Please try again.');
    }
  };

  const handleLeaveGroup = async (group_id) => {
    try {
      const group = groups.find(g => g.group_id === group_id);
      const updatedMembers = {
        members: group.members.filter(member => member !== loggedUser.user_id)
      };

      const response = await fetch(`${apiBaseGroups}/${loggedUser.user_id}/study-group/${group_id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${loggedUser.jwt_token}`,
          'Google-Token': `${loggedUser.credentials}`
        },
        body: JSON.stringify(updatedMembers)
      });

      if (!response.ok) {
        const errorData = await response.text();
        console.error('API Error:', response.status, errorData);
        throw new Error(`API error: ${response.status}`);
      }

      setFetchedGroups(prevGroups => 
        prevGroups.map(group => {
          if (group.group_id === group_id) {
            return { ...group, members: group.members.filter(p => p !== loggedUser.user_id) };
          }
          return group;
        })
      );

    } catch (error) {
      console.error('Error leaving group:', error);
      alert('Failed to leave group. Please try again.');
    }
  };

  const handleDeleteGroup = async (group) => {
    const group_id = group.group_id
    console.log('group', group)
    try {
      const response = await fetch(`${apiBaseGroups}/${loggedUser.user_id}/study-group/${group_id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${loggedUser.jwt_token}`,
          'Google-Token': `${loggedUser.credentials}`
        }
      });
      
      if (!response.ok) {
        const errorData = await response.text();
        console.error('API Error:', response.status, errorData);
        throw new Error(`API error: ${response.status}`);
      }

      setFetchedGroups(prevGroups => prevGroups.filter(group => group.group_id !== group_id));
      dispatch(deleteGroup(group_id));
      console.log('Group deleted successfully');
      alert('Group deleted successfully');
    } catch (error) {
      console.error('Error deleting group:', error);
      alert('Failed to delete group. Please try again.');
    }
  };

  const handleEditGroup = (group) => {
    const group_id = group.group_id
    console.log('edit group', group)
    const groupToEdit = groups.find(group => group.group_id === group_id);
    if (groupToEdit) {
      setNewGroup(groupToEdit);
      setIsEditing(true);
    }
  };

  const handleParticipantClick = (participant) => {
    if (participant !== loggedUser.user_id) {
      navigate(`/messages?user=${participant}`);
    }
  };

  const filteredGroups = groups.filter(group =>
    (group.group_name?.toLowerCase() || '').includes(searchTerm.toLowerCase()) ||
    (group.course_id?.toString().toLowerCase() || '').includes(searchTerm.toLowerCase()) ||
    (group.members || []).some(member => 
      (member?.toLowerCase() || '').includes(searchTerm.toLowerCase())
    )
  );

  const today = new Date().toISOString().split('T')[0];

  return (
    <div className="study-groups">
      <h2>Study Groups</h2>
      
      <div className="create-group">
        <h3>Create a New Group</h3>
        <form onSubmit={handleCreateGroup}>
          <input
            type="text"
            name="group_name"
            value={newGroup.group_name}
            onChange={handleInputChange}
            placeholder="Group Name"
            required
          />
          <select
            name="course_id"
            value={newGroup.course_id}
            onChange={handleInputChange}
            required
          >
            <option value="">Select Subject</option>
            {Array.isArray(courses) && courses.map((course, index) => (
              <option key={index} value={course}>
                {course}
              </option>
            ))}
          </select>
          <div className="datetime-inputs">
            <input
              type="date"
              name="meeting_date"
              value={newGroup.meeting_date}
              onChange={handleInputChange}
              placeholder="Meeting Date"
              min={today}
              required
            />
            <input
              type="time"
              name="start_time"
              value={newGroup.start_time}
              onChange={handleInputChange}
              placeholder="Start Time"
              required
            />
            <input
              type="time"
              name="end_time"
              value={newGroup.end_time}
              onChange={handleInputChange}
              placeholder="End Time"
              min={newGroup.start_time}
              required
            />
          </div>
          <div className="recurrence-options">
            <label>
              <input
                type="checkbox"
                name="is_recurring"
                checked={newGroup.is_recurring}
                onChange={handleInputChange}
              />
              Recurrent Meeting
            </label>
            {newGroup.is_recurring && (
              <>
                <select
                  name="recurrence_frequency"
                  value={newGroup.recurrence_frequency}
                  onChange={handleInputChange}
                  className="recurrence-dropdown"
                >
                  <option value="None">Select Frequency</option>
                  <option value="Daily">Daily</option>
                  <option value="Weekly">Weekly</option>
                  <option value="Monthly">Monthly</option>
                </select>
                <input
                  type="date"
                  name="recurrence_end_date"
                  value={newGroup.recurrence_end_date}
                  onChange={handleInputChange}
                  placeholder="Recurrence End Date"
                  min={newGroup.meeting_date}
                  required={newGroup.is_recurring}
                />
                {dateError && <p className="error-message">{dateError}</p>}
              </>
            )}
          </div>
          <button type="submit">{isEditing ? 'Save Updates' : 'Create Group'}</button>
        </form>
      </div>

      <div className="search-groups">
        <input
          type="text"
          placeholder="Search groups or participants"
          value={searchTerm}
          onChange={handleSearch}
        />
      </div>

      <div className="group-list">
        <h3>Existing Groups</h3>
        <ul>
          {filteredGroups.map((group) => (
            <li key={group.group_id} className="group-item">
              <div className="group-item-content">
                <h4>{group.group_name}</h4>
                <p>Subject: {group.course_id?.split(' - ')[1] || group.course_id}</p>
                <p>Date: {group.meeting_date}</p>
                <p>Time: {group.start_time} - {group.end_time}</p>
                {group.is_recurring && <p>Recurrence: {group.recurrence_frequency} until {group.recurrence_end_date}</p>}
                <p>Participants:&nbsp;
                  {group.members.map((participant, index) => (
                    <span key={index} 
                          className={`participant ${participant === loggedUser.user_id ? 'current-user-participant' : ''}`}
                          onClick={() => handleParticipantClick(participant)}>
                      {participant}
                      {index < group.members.length - 1 ? ', ' : ''}
                    </span>
                  ))}
                </p>
              </div>
              <div className="actions">
                {group.members.includes(loggedUser.user_id) ? (
                  <button onClick={() => handleLeaveGroup(group.group_id)} className="leave-button">Leave Group</button>
                ) : (
                  <button onClick={() => handleJoinGroup(group.group_id)} className="join-button">Join Group</button>
                )}
                {group.created_by === loggedUser.user_id && (
                  <>
                    <button onClick={() => handleEditGroup(group)} className="edit-button gray-button">Edit Group</button>
                    <button onClick={() => handleDeleteGroup(group)} className="delete-button gray-button">Delete Group</button>
                  </>
                )}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default StudyGroups;
