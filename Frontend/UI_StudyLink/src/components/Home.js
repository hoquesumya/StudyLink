import React from 'react';
import GroupStudy from '../assets/GroupStudy.png';
import './Home.css';

function Home() {
  return (
    <div className="home-container">
      <header className="home-header">
        <h1>StudyLink</h1>
      </header>
      <main className="home-main">
        <section className="hero-section">
          <div className="hero-content">
            <h2>Connect, Collaborate, and Excel in Your Studies</h2>
            <p>Join StudyLink to form study groups, share resources, and boost your academic performance.</p>
          </div>
          <div className="hero-image">
            <img src={GroupStudy} alt="Students collaborating" />
          </div>
        </section>
        <section className="features-section">
          <div className="feature-card">
            <i className="feature-icon message-icon"></i>
            <h3>Messaging</h3>
            <p>Communicate directly with fellow students or entire study groups.</p>
          </div>
          <div className="feature-card">
            <i className="feature-icon calendar-icon"></i>
            <h3>Calendar</h3>
            <p>Organize your study sessions, exams, and assignment deadlines.</p>
          </div>
          <div className="feature-card">
            <i className="feature-icon group-icon"></i>
            <h3>Study Groups</h3>
            <p>Create or join study groups based on your courses or interests.</p>
          </div>
        </section>
      </main>
      <footer className="home-footer">
        <p>&copy; 2024 StudyLink. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default Home;
