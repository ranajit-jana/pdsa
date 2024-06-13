import React, { useState, useEffect } from 'react';
import { Form, Input, Button, Select, Table, Row, Col, message } from 'antd';
import { getRules, createRule, updateRule, getPIIEntities } from '../api'; // Import API methods
import './Page2.css';

const { Option } = Select;
const { TextArea } = Input;

const Page2 = () => {
  const [form] = Form.useForm();
  const [dataSource, setDataSource] = useState([]);
  const [entityOptions, setEntityOptions] = useState([]);
  const [selectedRecordKey, setSelectedRecordKey] = useState(null);
  const [entityMap, setEntityMap] = useState({}); // Create a state to hold the mapping of entity IDs to names

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [rulesData, entitiesData] = await Promise.all([getRules(), getPIIEntities()]);

      // Create a mapping of entity IDs to entity names
      const entityMap = {};
      entitiesData.forEach(entity => {
        entityMap[entity.entity_id] = entity.entity_name;
      });
      setEntityMap(entityMap);

      setDataSource(rulesData.map((item) => ({
        key: item.rule_id, // Ensure this matches the unique identifier from the API
        ruleName: item.rule_name,
        combination: Array.isArray(item.entity_names) ? item.entity_names.map(id => entityMap[id]).join(', ') : '',
        description: item.rule_description,
        score: item.rule_score,
      })));

      setEntityOptions(entitiesData.map(entity => ({
        value: entity.entity_id,
        label: entity.entity_name
      })));

    } catch (error) {
      message.error('Failed to fetch data');
      console.error('Fetch Error:', error);
    }
  };

  const handleFinish = async (values) => {
    try {
      const payload = {
        rule_name: values.rule_name,
        entity_ids: values.entity_names,
        rule_description: values.rule_description,
        score: values.rule_score,
        rule_category: values.rule_category, // Include this field
      };

      if (selectedRecordKey !== null) {
        // Update existing rule
        const updatedRule = await updateRule(selectedRecordKey, payload);

        const updatedDataSource = dataSource.map((record) =>
          record.key === selectedRecordKey
            ? {
              ...record,
              ruleName: updatedRule.rule_name,
              combination: Array.isArray(updatedRule.entity_ids) ? updatedRule.entity_ids.map(id => entityMap[id]).join(', ') : '',
              description: updatedRule.rule_description,
              score: updatedRule.rule_score,
            }
            : record
        );
        setDataSource(updatedDataSource);
        message.success('Rule updated successfully');
      } else {
        // Create new rule
        const newRule = await createRule(payload);

        setDataSource([
          ...dataSource,
          {
            key: newRule.rule_id, // Ensure this matches the unique identifier from the API
            ruleName: newRule.rule_name,
            combination: Array.isArray(newRule.entity_ids) ? newRule.entity_ids.map(id => entityMap[id]).join(', ') : '',
            description: newRule.rule_description,
            score: newRule.rule_score,
          },
        ]);
        message.success('Rule created successfully');
      }
      form.resetFields();
      setSelectedRecordKey(null);
    } catch (error) {
      message.error('Failed to save rule');
      console.error('Save Error:', error);
    }
  };

  const handleCancel = () => {
    form.resetFields();
    setSelectedRecordKey(null);
  };

  const handleEdit = (key) => {
    const record = dataSource.find((item) => item.key === key);
    form.setFieldsValue({
      rule_name: record.ruleName,
      rule_description: record.description,
      rule_score: record.score,
      entity_names: record.combination.split(', ').map(name => Object.keys(entityMap).find(key => entityMap[key] === name)),
    });
    setSelectedRecordKey(key);
  };

  const columns = [
    {
      title: 'Rule Name',
      dataIndex: 'ruleName',
      key: 'ruleName',
    },
    {
      title: 'Combination',
      dataIndex: 'combination',
      key: 'combination',
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
    },
    {
      title: 'Score',
      dataIndex: 'score',
      key: 'score',
    },
    {
      title: 'Action',
      key: 'action',
      render: (_, record) => (
        <Button type="link" onClick={() => handleEdit(record.key)}>
          Edit
        </Button>
      ),
    },
  ];

  return (
    <div>
      <h2>PII Detection and Toxicity Analyzer</h2>
      <Form form={form} layout="vertical" onFinish={handleFinish}>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              label="Rule Name"
              name="rule_name"
              rules={[{ required: true, message: 'Please enter a rule name!' }]}
            >
              <Input placeholder="Enter rule name" />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              label="Rule Category"
              name="rule_category"
              rules={[{ required: true, message: 'Please select a rule category!' }]}
            >
              <Select placeholder="Select a rule category">
                <Option value="ID">Identity</Option>
                <Option value="FI">Financial</Option>
                <Option value="PR">Personal</Option>
              </Select>
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              label="Rule Description"
              name="rule_description"
              rules={[{ required: true, message: 'Please enter a description!' }]}
            >
              <TextArea rows={2} placeholder="Enter description" />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              label="Rule Score"
              name="rule_score"
              rules={[{ required: true, message: 'Please select a score!' }]}
            >
              <Select placeholder="Select a score">
                {Array.from({ length: 10 }, (_, i) => (
                  <Option key={i + 1} value={i + 1}>{i + 1}</Option>
                ))}
              </Select>
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={24}>
            <Form.Item
              label="Entities Names"
              name="entity_names"
              rules={[{ required: true, message: 'Please select entity names!' }]}
            >
              <Select mode="multiple" placeholder="Select entity names">
                {entityOptions.map(option => (
                  <Option key={option.value} value={option.value}>{option.label}</Option>
                ))}
              </Select>
            </Form.Item>
          </Col>
        </Row>
        <Form.Item>
          <Button type="primary" htmlType="submit">
            Save
          </Button>
          <Button style={{ marginLeft: '10px' }} onClick={handleCancel}>
            Cancel
          </Button>
        </Form.Item>
      </Form>
      <Table columns={columns} dataSource={dataSource} />
    </div>
  );
};

export default Page2;
