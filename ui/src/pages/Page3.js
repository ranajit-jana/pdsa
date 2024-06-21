import React, { useState, useEffect } from 'react';
import { Select, Table, Typography } from 'antd';
import axios from 'axios';
import {
  getBlockRuleScores,
} from '../api';

const { Option } = Select;
const { Title, Paragraph } = Typography;

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
  
        // Calculate and display the case score total
        const totalScore = data.reduce((sum, item) => sum + item.score, 0);
        setCaseScoreTotal(totalScore);
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
        })
        .catch(error => console.error('Error fetching block_rule_scores:', error));
    }
  }, [selectedCase]);  

  const columns = [
    { title: 'Block', dataIndex: 'source', key: 'source' },
    { title: 'Score', dataIndex: 'score', key: 'score' },
    { title: 'Rule Match', dataIndex: 'rules_match', key: 'rules_match' },
  ];

  return (
    <div className="container">
      <h2>Case Overview</h2>
      <br/>
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
      <br/>
      <br/>
      <div className="summary">
        <Paragraph><strong>Case Score Total:</strong> {caseScoreTotal}</Paragraph>
        <br/>
        <Paragraph><strong>Case total Blocks:</strong> {totalBlocks}</Paragraph>
      </div>
      <br/>
      <br/>
      <br/>
      <div className="table">
        <Table
          columns={columns}
          dataSource={blocks}
          rowKey="block_hash"
          pagination={false}
        />
      </div>

      {/* Add some spacing at the bottom */}
      <div style={{ height: '50px' }}></div>
    </div>
  );
};

export default Page3;
