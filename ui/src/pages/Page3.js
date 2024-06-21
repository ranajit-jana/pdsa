import React, { useState, useEffect } from 'react';
import { Select, Table, Typography, Tag } from 'antd';
import { getBlockRuleScores } from '../api';

const { Option } = Select;
const { Paragraph } = Typography;

const Page3 = () => {
  const [caseNames, setCaseNames] = useState([]);
  const [selectedCase, setSelectedCase] = useState('');
  const [caseScoreTotal, setCaseScoreTotal] = useState(0);
  const [totalBlocks, setTotalBlocks] = useState(0);
  const [blocks, setBlocks] = useState([]);

  useEffect(() => {
    // Fetch all block_rule_scores
    getBlockRuleScores()
      .then(data => {
        const uniqueCaseNames = [...new Set(data.map(item => item.case_name))];
        setCaseNames(uniqueCaseNames);
      })
      .catch(error => console.error('Error fetching block_rule_scores:', error));
  }, []);

  useEffect(() => {
    if (selectedCase) {
      // Fetch blocks for the selected case
      getBlockRuleScores()
        .then(data => {
          const filteredData = data.filter(item => item.case_name === selectedCase);
          setBlocks(filteredData);
          setTotalBlocks(filteredData.length);
          // Calculate and display the case score total for the selected case
          const totalScore = filteredData.reduce((sum, item) => sum + item.score, 0);
          setCaseScoreTotal(totalScore);
        })
        .catch(error => console.error('Error fetching block_rule_scores:', error));
    }
  }, [selectedCase]);

  const getScoreColor = (score) => {
    if (score >= 1 && score <= 4) {
      return '#000000'; // black
    } else if (score >= 5 && score <= 7) {
      return '#FF0000'; // red
    } else if (score >= 8 && score <= 10) {
      return '#8B0000'; // dark red
    }
    return '#000000'; // default color
  };

  const columns = [
    { title: 'Source', dataIndex: 'source', key: 'source' },
    {
      title: 'Score',
      dataIndex: 'score',
      key: 'score',
      render: score => (
        <span style={{ color: getScoreColor(score) }}>
          {score}
        </span>
      )
    },
    {
      title: 'Rule Match',
      dataIndex: 'rules_match',
      key: 'rules_match',
      render: rules_match => {
        // Split the string into an array
        const rulesArray = rules_match ? rules_match.split(',') : [];
        return (
          <>
            {rulesArray.map(rule => (
              <Tag key={rule} style={{ margin: '0 5px 5px 0' }}>{rule}</Tag>
            ))}
          </>
        );
      }
    },
  ];

  return (
    <div className="container">
      <h2>Case Overview</h2>
      <br />
      <div className="dropdown">
        <label htmlFor="caseSelect">Select Case: </label>
        <Select
          id="caseSelect"
          style={{ width: 200 }}
          onChange={value => setSelectedCase(value)}
        >
          {caseNames.map(caseName => (
            <Option key={caseName} value={caseName}>
              {caseName}
            </Option>
          ))}
        </Select>
      </div>
      <br />
      <br />
      <div className="summary">
        <Paragraph>
          <strong>Case Score Total:</strong>
          <span style={{ color: getScoreColor(caseScoreTotal) }}> {caseScoreTotal}</span>
        </Paragraph>
        <br />
        <Paragraph><strong>Case total Blocks:</strong> {totalBlocks}</Paragraph>
      </div>
      <br />
      <br />
      <br />
      <div className="table">
        <Table
          columns={columns}
          dataSource={blocks}
          rowKey="source" // Changed from "block_hash" to "source"
          pagination={false}
        />
      </div>

      {/* Add some spacing at the bottom */}
      <div style={{ height: '50px' }}></div>
    </div>
  );
};

export default Page3;
