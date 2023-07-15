-- SQL script to create a stored procedure to ComputeAverageScoreForUserSQL script that creates and store average score for students

CREATE PROCEDURE ComputeAverageScoreForUser (user_id INT)
BEGIN
    
    DECLARE sum_score INT;
    DECLARE count_corrections INT;
    DECLARE avg_score FLOAT;

    SELECT SUM(score), COUNT(*) INTO sum_score, count_corrections
    FROM corrections
    WHERE user_id = user_id;

   
    IF count_corrections > 0 THEN
        SET avg_score = sum_score / count_corrections;
    ELSE
        SET avg_score = 0;
    END IF;

  
    UPDATE users
    SET average_score = avg_score
    WHERE id = user_id;
END //

DELIMITER ;
