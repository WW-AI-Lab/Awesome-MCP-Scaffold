"""
数据分析提示模块

提供数据分析和处理相关的 MCP 提示模板。
"""

from mcp.server.fastmcp import FastMCP


def register_analysis_prompts(mcp: FastMCP) -> None:
    """注册数据分析相关的提示模板"""

    @mcp.prompt(title="Data Analysis")
    def data_analysis(data_description: str, analysis_goals: str = "") -> str:
        """
        Generate a prompt for comprehensive data analysis.
        
        Args:
            data_description: Description of the dataset
            analysis_goals: Specific analysis objectives
        """
        prompt = f"""Please conduct a comprehensive analysis of the following dataset:

**Dataset Description:**
{data_description}
"""

        if analysis_goals:
            prompt += f"""
**Analysis Goals:**
{analysis_goals}
"""

        prompt += """
Please provide:

1. **Exploratory Data Analysis (EDA)**:
   - Data structure and types
   - Missing values analysis
   - Basic statistical summaries
   - Data quality assessment

2. **Descriptive Statistics**:
   - Central tendency measures
   - Variability measures
   - Distribution analysis
   - Outlier detection

3. **Data Visualization Recommendations**:
   - Appropriate chart types
   - Key visualizations to create
   - Dashboard design suggestions

4. **Pattern Discovery**:
   - Trends and seasonality
   - Correlations and relationships
   - Anomalies and outliers

5. **Insights and Findings**:
   - Key observations
   - Business implications
   - Actionable recommendations

6. **Next Steps**:
   - Further analysis suggestions
   - Data collection recommendations
   - Model development opportunities

Please provide specific, data-driven insights with supporting evidence."""

        return prompt

    @mcp.prompt(title="Statistical Analysis")
    def statistical_analysis(hypothesis: str, data_info: str) -> str:
        """
        Generate a prompt for statistical hypothesis testing.
        
        Args:
            hypothesis: The hypothesis to test
            data_info: Information about the available data
        """
        return f"""Please design and conduct a statistical analysis to test the following hypothesis:

**Hypothesis:**
{hypothesis}

**Available Data:**
{data_info}

Please provide:

1. **Hypothesis Formulation**:
   - Null hypothesis (H₀)
   - Alternative hypothesis (H₁)
   - Significance level (α)

2. **Test Selection**:
   - Appropriate statistical test
   - Assumptions and requirements
   - Justification for test choice

3. **Data Preparation**:
   - Data cleaning requirements
   - Sample size considerations
   - Variable transformations

4. **Analysis Plan**:
   - Step-by-step methodology
   - Software/tools recommendations
   - Expected outputs

5. **Interpretation Guidelines**:
   - How to interpret results
   - P-value interpretation
   - Effect size considerations

6. **Reporting Template**:
   - Results presentation format
   - Confidence intervals
   - Practical significance

Please provide a complete analysis framework with code examples where applicable."""

    @mcp.prompt(title="Predictive Modeling")
    def predictive_modeling(target_variable: str, features_description: str, business_context: str = "") -> str:
        """
        Generate a prompt for predictive modeling project.
        
        Args:
            target_variable: The variable to predict
            features_description: Description of available features
            business_context: Business context and requirements
        """
        prompt = f"""Please design a predictive modeling solution for the following scenario:

**Target Variable:**
{target_variable}

**Available Features:**
{features_description}
"""

        if business_context:
            prompt += f"""
**Business Context:**
{business_context}
"""

        prompt += """
Please provide:

1. **Problem Definition**:
   - Problem type (regression, classification, etc.)
   - Success metrics
   - Business constraints

2. **Data Strategy**:
   - Feature engineering opportunities
   - Data preprocessing requirements
   - Train/validation/test split strategy

3. **Model Selection**:
   - Candidate algorithms
   - Model complexity considerations
   - Baseline model recommendations

4. **Evaluation Framework**:
   - Appropriate metrics
   - Cross-validation strategy
   - Model comparison approach

5. **Implementation Plan**:
   - Development timeline
   - Resource requirements
   - Deployment considerations

6. **Monitoring and Maintenance**:
   - Model performance tracking
   - Retraining schedule
   - Drift detection

Please provide a comprehensive modeling strategy with practical recommendations."""

        return prompt

    @mcp.prompt(title="Data Quality Assessment")
    def data_quality_assessment(dataset_info: str) -> str:
        """
        Generate a prompt for data quality evaluation.
        
        Args:
            dataset_info: Information about the dataset to assess
        """
        return f"""Please conduct a comprehensive data quality assessment for the following dataset:

**Dataset Information:**
{dataset_info}

Please evaluate and report on:

1. **Completeness**:
   - Missing value analysis
   - Data coverage assessment
   - Completeness by field/time period

2. **Accuracy**:
   - Data validation checks
   - Outlier detection
   - Consistency with business rules

3. **Consistency**:
   - Format standardization
   - Cross-field validation
   - Temporal consistency

4. **Validity**:
   - Data type validation
   - Range and constraint checks
   - Referential integrity

5. **Uniqueness**:
   - Duplicate detection
   - Primary key validation
   - Deduplication strategies

6. **Timeliness**:
   - Data freshness
   - Update frequency
   - Latency analysis

7. **Data Quality Issues**:
   - Identified problems
   - Impact assessment
   - Remediation recommendations

8. **Quality Improvement Plan**:
   - Immediate fixes
   - Process improvements
   - Monitoring framework

Please provide specific, actionable recommendations for improving data quality."""
