-- SQL script to create a stored procedure ComputeAverageScoreForUser

DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    -- Declare variables for sum_score and count_corrections
    DECLARE sum_score INT;
    DECLARE count_corrections INT;
    DECLARE avg_score FLOAT;

    -- Compute the sum of scores and count of corrections for the user
    SELECT SUM(score), COUNT(*) INTO sum_score, count_corrections
    FROM corrections
    WHERE user_id = user_id;

    -- Compute the average score
    IF count_corrections > 0 THEN
        SET avg_score = sum_score / count_corrections;
    ELSE
        SET avg_score = 0;
    END IF;

    -- Update the average_score for the user
    UPDATE users
    SET average_score = avg_score
    WHERE id = user_id;
END //

DELIMITER ;
