-- SQL script to create a stored procedure AddBonus

DELIMITER //

CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name VARCHAR(255), IN score INT)
BEGIN
    -- Declare variables for project_id and existing_project_count
    DECLARE project_id INT;
    DECLARE existing_project_count INT;

    -- Check if the project exists
    SELECT COUNT(*) INTO existing_project_count FROM projects WHERE name = project_name;

    IF existing_project_count = 0 THEN
        -- Create the project if it doesn't exist
        INSERT INTO projects (name) VALUES (project_name);
        SET project_id = LAST_INSERT_ID();
    ELSE
        -- Get the project_id if it already exists
        SELECT id INTO project_id FROM projects WHERE name = project_name;
    END IF;

    -- Add the bonus correction
    INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, project_id, score);
END //

DELIMITER ;

