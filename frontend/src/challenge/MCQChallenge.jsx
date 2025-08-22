import React from 'react';
import { useState } from 'react';


export function MCQChallenge({ challenge, showExplanation }) {
    const [selectedOption, setSelectedOption] = useState(null);
    const [shouldShowExplanation, setShouldShowExplanation] = useState(showExplanation);

    const options = typeof challenge.options === "string" ? JSON.parse(challenge.options) : challenge.options

    const handleOptionSelect = (index) => {
        if (selectedOption !== null) return;
        setSelectedOption(index)
        setShouldShowExplanation(true)
    }

    // checks if the selected answer is correct or not
    const getOptionClass = (index) => {
        if (selectedOption === null) return "option"

        // you highlight the correct answer regardless of what the user selected
        if (index === challenge.correct_answer_id) {
            return "option correct";
        }

        if (selectedOption === index && index !== challenge.correct_answer_id) {
            return "option incorrect";
        }

        return "option";
    }

    return (
        <div className='challenge-display'>
            <p><strong>Difficulty</strong>: {challenge.difficulty}</p>
            <p className='challenge-title'>{challenge.title}</p>
            <div className='options'>
                {/* NOTE: key is used to uniquely identify the elements of the arr - it gives each option a unique identifier to efficiently update and re-render */}
                {options.map((option, index) => (
                    <div
                        className={getOptionClass(index)}
                        key={index}
                        onClick={() => handleOptionSelect(index)}
                    >
                        {option}

                    </div>
                ))}
            </div>
            {shouldShowExplanation && selectedOption !== null && (
                <div className='explanation'>
                    <h4>Explanation</h4>
                    <p>{challenge.explanation}</p>
                </div>
            )}
        </div>
    )
}