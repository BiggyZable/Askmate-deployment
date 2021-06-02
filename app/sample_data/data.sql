DROP TABLE IF EXISTS question CASCADE;
DROP TABLE IF EXISTS answer CASCADE;
DROP TABLE IF EXISTS comment CASCADE;
DROP TABLE IF EXISTS tag CASCADE;
DROP TABLE IF EXISTS question_tag CASCADE;
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users
(
    id              SERIAL PRIMARY KEY,
    username        VARCHAR(30) NOT NULL UNIQUE,
    password        VARCHAR(300) NOT NULL,
    reg_time        TIMESTAMP DEFAULT NOW()::timestamp (0),
    reputation      INTEGER
);

CREATE TABLE question
(
   id              SERIAL PRIMARY KEY
  ,submission_time TIMESTAMP DEFAULT NOW()::timestamp (0)
  ,view_number     INTEGER  NOT NULL
  ,vote_number     INTEGER  NOT NULL
  ,title           VARCHAR(255) NOT NULL
  ,message         VARCHAR(500) NOT NULL
  ,image           VARCHAR(100)
  ,user_id         INTEGER REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE answer
(
   id              SERIAL PRIMARY KEY
  ,submission_time TIMESTAMP DEFAULT NOW()::timestamp(0)
  ,vote_number     INTEGER  NOT NULL
  ,question_id     INTEGER REFERENCES question(id) ON DELETE CASCADE
  ,message         VARCHAR(500) NOT NULL
  ,image           VARCHAR(100)
  ,user_id         INTEGER REFERENCES users(id) ON DELETE CASCADE
  ,accepted        BOOLEAN DEFAULT FALSE
);

CREATE TABLE comment
(
    id              SERIAL PRIMARY KEY,
    question_id     INTEGER REFERENCES question(id) ON DELETE CASCADE,
    answer_id       INTEGER REFERENCES answer(id) ON DELETE CASCADE,
    message         VARCHAR(500) NOT NULL,
    submission_time TIMESTAMP DEFAULT NOW()::timestamp(0),
    edited_number   INTEGER NOT NULL DEFAULT 0,
    user_id         INTEGER REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE tag
(
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL
);

CREATE TABLE question_tag
(
    question_id     INTEGER REFERENCES question(id) ON DELETE CASCADE,
    tag_id          INTEGER REFERENCES tag(id) ON DELETE CASCADE
);

INSERT INTO question(submission_time, view_number, vote_number, title, message, image)
VALUES  ('2010-10-01 10:10:10', 13 ,7,'How to make lists in Python?','I am totally new to this, any hints?',NULL),
        ('2010-10-01 10:10:10',15,9,'Wordpress loading multiple jQuery Versions','I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(''.myBook'').booklet();

I could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.

BUT in my theme i also using jquery via webpack so the loading order is now following:

jquery
booklet
app.js (bundled file with webpack, including jquery)','images/image1.png'),
       ('2010-10-01 10:10:10',1364,57,'Drawing canvas with an image picked with Cordova Camera Plugin','I''m getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I''m on IOS, it throws errors such as cross origin issue, or that I''m trying to use an unknown format.

This is the code I''m using to draw the image (that works on web/desktop but not cordova built ios app)',NULL);

INSERT INTO answer(submission_time, vote_number, question_id, message, image)
VALUES  ('2010-10-01 10:10:10',4,1,'You need to use brackets: my_list = []',NULL),
        ('2010-10-01 10:10:10',35,1,'Look it up in the Python docs',NULL);
