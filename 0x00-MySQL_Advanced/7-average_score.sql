-- Procedure: ComputeAverageScoreForUser
-- Description: Computes and stores the average score for a student
-- Input: user_id - a users.id value

DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE num_scores INT;

    -- Calculate the total score and the number of scores for the specified user
    SELECT SUM(score), COUNT(*) INTO total_score, num_scores
    FROM corrections
    WHERE user_id = user_id;

    -- Update the average_score column if there are scores available for the user
    IF num_scores > 0 THEN
        UPDATE users
        SET average_score = total_score / num_scores
        WHERE id = user_id;
    END IF;
END //

DELIMITER ;
