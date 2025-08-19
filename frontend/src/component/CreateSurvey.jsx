import { useCreateSurveyProvider } from "./CreateSurveyProvider";
import React, { useEffect, useState } from "react";
import { PlusIcon2 } from "./Icons";
import QuestionList from "./QuestionList";
import { motion } from "framer-motion";
import { FaMagic } from "react-icons/fa";
import ApiService from "../services/apiService";

const CreateSurvey = () => {
  const {
    questions,
    defaultQuestionType,
    setSurveyTitle,
    setSurveyDescription,
    surveyTitle,
    surveyDescription,
    addNewQuestion,
  } = useCreateSurveyProvider();

  const [titleLength, setTitleLength] = useState(0);
  const [descriptionLength, setDescriptionLength] = useState(0);
  const [titleError, setTitleError] = useState("");
  const [descriptionError, setDescriptionError] = useState("");

  const [isGenerating, setIsGenerating] = useState(false);
  const [generationError, setGenerationError] = useState("");
  const [generationSuccess, setGenerationSuccess] = useState("");

  useEffect(() => {
    setTitleLength(surveyTitle?.length || 0);
    setDescriptionLength(surveyDescription?.length || 0);
  }, [surveyTitle, surveyDescription]);

  const handleGenerateSurvey = async () => {
    if (!surveyTitle || !surveyDescription) {
      setGenerationError("Please provide both title and description");
      return;
    }

    setIsGenerating(true);
    setGenerationError("");
    setGenerationSuccess("");

    try {
      const generatedSurvey = await ApiService.generateSurvey({
        title: surveyTitle,
        description: surveyDescription,
      });

      console.log("Generated survey:", generatedSurvey);

      setGenerationSuccess(
        "Survey generated successfully! Check the console for details."
      );

      // TODO: Handle the generated survey data
      // This will be implemented when we connect it to the survey provider
    } catch (error) {
      console.error("Failed to generate survey:", error);
      setGenerationError("Failed to generate survey. Please try again.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="flex h-full font-switzer lg:overflow-auto scrollbar-style flex-col gap-4 sm:gap-6 sm:p-4">
      <div className="flex flex-col space-y-6">
        {/* Title Input */}
        <motion.div
          whileHover={{ boxShadow: "0 4px 12px rgba(0, 0, 0, 0.05)" }}
          className="rounded-[12px] shadow-sm w-full border border-[#00000020] bg-white flex flex-col transition-all duration-300"
        >
          <motion.input
            type="text"
            maxLength={100}
            name="title"
            value={surveyTitle}
            onChange={(e) => {
              const value = e.target.value;
              setSurveyTitle(value);
              setTitleLength(value.length);
              setTitleError(
                value.length >= 100 ? "Title cannot exceed 100 characters." : ""
              );
            }}
            placeholder="Enter survey title"
            className="text-[16px] px-5 pt-4 pb-1 text-primary outline-none border-none bg-transparent rounded-t-[12px] transition-all duration-200"
          />
          <div className="px-5 pb-3 text-right">
            <p
              className={`text-[10px] ${
                titleLength > 90 ? "text-amber-500" : "text-gray-400"
              }`}
            >
              {titleLength}/100
            </p>
            {titleError && <p className="text-red-500 text-sm">{titleError}</p>}
          </div>
        </motion.div>

        {/* Description Input */}
        <motion.div
          whileHover={{ boxShadow: "0 4px 12px rgba(0, 0, 0, 0.05)" }}
          className="rounded-[12px] shadow-sm w-full border border-[#00000020] bg-white flex flex-col transition-all duration-300"
        >
          <motion.input
            type="text"
            placeholder="Enter survey description"
            maxLength={500}
            name="description"
            value={surveyDescription}
            onChange={(e) => {
              const value = e.target.value;
              setSurveyDescription(value);
              setDescriptionLength(value.length);
              setDescriptionError(
                value.length >= 500
                  ? "Description cannot exceed 500 characters."
                  : ""
              );
            }}
            className="text-[16px] px-5 pt-4 pb-1 text-primary outline-none border-none bg-transparent rounded-t-[12px] transition-all duration-200"
          />
          <div className="px-5 pb-3 text-right">
            <p
              className={`text-[10px] ${
                descriptionLength > 490 ? "text-amber-500" : "text-gray-400"
              }`}
            >
              {descriptionLength}/500
            </p>
            {descriptionError && (
              <p className="text-red-500 text-xs">{descriptionError}</p>
            )}
          </div>
        </motion.div>
      </div>

      {/* Question List */}
      <div className="flex-1">
        <QuestionList questions={questions} />
      </div>

      {/* Add Question Button */}
      <motion.div
        whileHover={{ scale: 1.01, borderColor: "#6851a7 " }}
        className="border-2 py-4 md:py-5 lg:py-6 rounded-[12px] flex justify-center gap-4 border-dotted border-[#6851a7] bg-[#6851a7]/5 transition-all duration-300"
      >
        <motion.button
          whileHover={{
            scale: 1.05,
            boxShadow: "0 8px 25px rgba(147, 51, 234, 0.4)",
          }}
          whileTap={{ scale: 0.95 }}
          onClick={handleGenerateSurvey}
          disabled={isGenerating}
          className={`bg-gradient-to-r from-purple-700 via-purple-600 to-indigo-700 hover:from-purple-600 hover:via-purple-500 hover:to-indigo-600 flex gap-2 items-center text-white py-3 px-6 rounded-full shadow-lg transition-all duration-300 ${
            isGenerating ? "opacity-70 cursor-not-allowed" : ""
          }`}
        >
          <FaMagic
            className={`h-4 w-4 ${isGenerating ? "animate-spin" : ""}`}
          />
          <span className="font-medium text-base">
            {isGenerating ? "Generating..." : "Generate Survey"}
          </span>
        </motion.button>
        <motion.button
          whileHover={{
            scale: 1.05,
            boxShadow: "0 6px 20px rgba(108, 93, 211, 0.3)",
          }}
          whileTap={{ scale: 0.95 }}
          onClick={() => addNewQuestion(defaultQuestionType)}
          className="bg-[#6851a7] flex gap-2 items-center text-white py-3 px-6 rounded-full shadow-sm transition-all duration-300"
        >
          <PlusIcon2 className="h-4 w-4" />
          <span className="font-medium text-base">Add Question</span>
        </motion.button>
      </motion.div>

      {/* Success Display */}
      {generationSuccess && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-green-50 border border-green-200 rounded-lg p-3 text-green-700 text-sm"
        >
          <p className="font-medium">Success:</p>
          <p>{generationSuccess}</p>
        </motion.div>
      )}

      {/* Error Display */}
      {generationError && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-red-50 border border-red-200 rounded-lg p-3 text-red-700 text-sm"
        >
          <p className="font-medium">Error:</p>
          <p>{generationError}</p>
        </motion.div>
      )}
    </div>
  );
};

export default CreateSurvey;
