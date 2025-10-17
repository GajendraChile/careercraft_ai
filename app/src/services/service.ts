
const API_ENDPOINT_URL = `${process.env.REACT_APP_API_URI}/planner_agent/`; // Replace with your actual API base URL

export async function searchProfiles(postData: any): Promise<string> {
    try {
      const response = await fetch(`${API_ENDPOINT_URL}`, 
        { // Replace with your API endpoint
            method: 'POST',
            // headers: {
            // 'Content-Type': 'application/json',
            // // Add any other headers, like authorization tokens, if needed
            // },
            body: postData,
        }
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error in GET request:', error);
      throw error; // Re-throw to be handled by the component
    }
}