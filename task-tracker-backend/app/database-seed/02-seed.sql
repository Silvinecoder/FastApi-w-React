
CREATE TABLE "user" (
	uuid UUID NOT NULL, 
	email VARCHAR(30) NOT NULL, 
	password_hash VARCHAR(100) NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (uuid), 
	UNIQUE (uuid)
);

CREATE TABLE task (
	uuid UUID NOT NULL, 
	title VARCHAR(50) NOT NULL,
	description VARCHAR(100), 
	is_complete BOOLEAN, 
	user_uuid UUID, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (uuid), 
	UNIQUE (uuid), 
	FOREIGN KEY(user_uuid) REFERENCES "user" (uuid)
);


-- Inserts

INSERT INTO "user" (uuid, email, password_hash) VALUES
  ('uuid-1', 'test@example.com', 'hashedpassword');
