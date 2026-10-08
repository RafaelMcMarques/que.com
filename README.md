# QUE.COM

**QUE.COM** is a web application for managing waiting queues. It allows businesses or service providers to create a queue and allows users to join it and monitor their position in real time.

A demonstration video can be found [here](https://www.youtube.com/watch?v=4rmdbmbZmKw).

The project was developed as my **CS50x Final Project**.

## Overview

The application follows a simple three-layer architecture:

- **Frontend** — Built with **HTML, CSS, and JavaScript**, providing the user interface for creating, joining, and managing queues.
- **Backend** — A **Flask** application written in Python handles routing, sessions, queue management, and communication between the frontend and database.
- **Database** — **SQLite** stores queues, users, positions, and queue information.

The backend connects the frontend to the database and manages the queue logic. Users can create a queue, share its ID with others, join the queue, and track their position. Queue owners can monitor the queue and call the next person when they are ready.

## Main Features

- Create and manage waiting queues
- Join an existing queue using its ID
- Track the user's current position
- Notify users when it is their turn
- Allow users to leave a queue
- Allow queue owners to call the next person
- Real-time position updates through backend endpoints

## Technologies

- **Python**
- **Flask**
- **SQLite**
- **HTML**
- **CSS**
- **JavaScript**
